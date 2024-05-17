import random
import time

from telebot.types import InlineKeyboardButton, Message, User, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from MODULES.constants.reg_variables.BOT import GUARD
from MODULES.constants.reg_variables.MORPH import MORPH
from MODULES.database.models.stories import Stories, Views
from MODULES.domain.pre_send.call_data_handler import Call
from MODULES.domain.pre_send.page_compiler import PageLoader
from MODULES.domain.executors.graph_loader import Graph

from MODULES.database.models.users import Authors, Stats


def no_bug(func):
    """
    При возникновении ошибки в процессе выполнения метода
    высылает сообщение с соответствующим текстом
    :param func: Метод, который передается в декоратор
    :return:
    """
    def inner(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            self.send(PageLoader(11)(str(e)).to_dict)

    return inner


def button(text, call_data) -> InlineKeyboardButton:
    return InlineKeyboardButton(text, callback_data=call_data)


class Exec(Call):
    def __init__(self, message: Message, user: User | None = None):
        self.message: Message = message
        self.user = message.from_user if user is None else user
        self.db_user = None
        self.load_db_user()

    @no_bug
    def load_db_user(self):
        """
        Загружает пользователя из базы данных;
        В случае отсутствия пользователя - создает запись
        :return:
        """
        try:
            self.db_user = Authors.get(tg_id=self.user.id)
        except Exception as e:
            db_not_found_error = e
            stat = Stats.create()
            data = {
                'tg_id': self.user.id,
                'username': self.user.username,
                'stat': stat
            }
            self.db_user = Authors.create(**data)

    def send(self, data: dict):
        """
        Отправляет новое сообщение
        :param data: Параметры нового сообщения
        :return:
        """
        GUARD.send_message(chat_id=self.message.chat.id, **data)

    def edit(self, data: dict):
        """
        Изменяет сообщение с ID объекта MESSAGE, переданного при инициализации класса
        :param data: Параметры нового сообщения
        :return:
        """
        try:
            GUARD.edit_message_text(chat_id=self.message.chat.id, message_id=self.message.id, **data)
        except Exception as e:
            self.send(PageLoader(11)(str(e)).to_dict)
            GUARD.edit_message_text(chat_id=self.message.chat.id, message_id=self.message.id+1, **data)

    @no_bug
    def cancel(self, page):
        """
        Отменяет next_step_handler и откатывается до предыдущей страницы
        :param page: Название метода (страницы), которая будет сгенерирована при вызове этого метода
        :return:
        """
        GUARD.clear_step_handler(self.message)
        page = getattr(self, page)
        page()

    @no_bug
    def start(self):
        """
        Страница бота - старт
        :return:
        """
        if self.db_user.is_regged:
            self.main()
            return
        self.send(PageLoader(1)().to_dict)

    @no_bug
    def add_author_name(self):
        """
        Страница бота - добавить псевдоним
        :return:
        """
        self.edit(PageLoader(2)().to_dict)
        GUARD.register_next_step_handler(self.message, callback=self.check_new_author_name)

    @no_bug
    def check_new_author_name(self, message):
        """
        Проверяет новое имя автора по нескольким критериям:

        1. Не длиннее 16 символов

        2. Уникальность

        При всех вердиктах вызывает соответствующие страницы
        :param message: Объект класса telebot.types.Message - сообщение пользователя с псевдонимом
        :return:
        """
        GUARD.delete_message(self.message.chat.id, message.id)
        if len(message.text) > 16:
            self.edit(PageLoader(3)().to_dict)
            return

        other = Authors.select().where((Authors.author_name == message.text) & (Authors.tg_id != self.db_user.tg_id))
        if other:
            self.edit(PageLoader(4)().to_dict)
            return

        self.db_user.author_name = message.text
        self.db_user.is_regged = True
        Authors.save(self.db_user)
        self.edit(PageLoader(5)().to_dict)

    @no_bug
    def main(self):
        """
        Страница бота - главная
        :return:
        """
        self.edit(PageLoader(6)(
            self.db_user.author_name,
            self.db_user.stat.views,
            self.db_user.stat.respect,
            str(round((self.db_user.stat.respect / (self.db_user.stat.views + (1 if self.db_user.stat.views == 0 else 0)))*100, 2)).ljust(4, "0")
        ).to_dict)

    @no_bug
    def change_author_name(self):
        """
        Страница бота - сменит псевдоним
        :return:
        """
        self.edit(PageLoader(7)().to_dict)
        GUARD.register_next_step_handler(self.message, callback=self.check_changed_author_name)

    @no_bug
    def check_changed_author_name(self, message):
        """
        Проверяет введенное имя автора по нескольким критериям:

        1. Не длиннее 16 символов

        2. Уникальность

        При всех вердиктах вызывает соответствующие страницы
        :param message: Объект класса telebot.types.Message - сообщение пользователя с псевдонимом
        :return:
        """
        GUARD.delete_message(self.message.chat.id, message.id)
        if len(message.text) > 16:
            self.edit(PageLoader(8)().to_dict)
            return

        other = Authors.select().where((Authors.author_name == message.text) & (Authors.tg_id != self.db_user.tg_id))
        if other:
            self.edit(PageLoader(9)().to_dict)
            return

        self.db_user.author_name = message.text
        Authors.save(self.db_user)
        pld = PageLoader(10)
        for i in range(5, -1, -1):
            self.edit(pld(message.text, i).to_dict)
            time.sleep(1)
        self.main()

    @no_bug
    def add_story(self):
        """
        Страница бота - добавить историю
        :return:
        """
        self.edit(PageLoader(12)().to_dict)
        GUARD.register_next_step_handler(self.message, callback=self.add_header)

    @no_bug
    def add_header(self, message):
        """
        Страница бота - добавить заголовок истории
        :param message: Объект класса telebot.types.Message с ответом пользователя
        :return:
        """
        GUARD.delete_message(self.message.chat.id, message.id)
        self.edit(PageLoader(13)().to_dict)
        GUARD.register_next_step_handler(self.message, self.check_text, message.text)

    @no_bug
    def check_text(self, message, title):
        """
        Проверяет текст истории на уникальность (При совпадении больше чем на 89% - история не добавляется)
        :param message: Объект класса telebot.types.Message с ответом пользователя
        :param title: Заголовок истории
        :return:
        """
        GUARD.delete_message(self.message.chat.id, message.id)
        stories = Stories.select()
        pld = PageLoader(14)
        grp = Graph(len(stories))
        for story in stories:
            same = 0
            for comp in zip(message.text.split(), story.text.split()):
                same += int(MORPH.parse(comp[0])[0].word == MORPH.parse(comp[1])[0].word)
            same_percent = (same / len(max([message.text.split(), story.text.split()], key=len))) * 100
            if same_percent < 89:
                grp += 1
                self.edit(pld(str(grp)).to_dict)
                continue
            self.final_add_story(False, '', '')
            return

        self.final_add_story(True, message.text, title)

    @no_bug
    def final_add_story(self, add: bool, text, title):
        """
        Заканчивает процесс добавления истории в бд
        :param add: Сохранить историю (при подозрениях на не уникальность текста False)
        :param text: Текст истории
        :param title: Заголовок истории
        :return:
        """
        new = Stories(
            text=text,
            title=title,
            author=self.db_user
        )
        if add:
            new.save()
        self.edit(PageLoader(15)().to_dict)

    @no_bug
    def next_story(self):
        """
        Высылает новую историю из бд для просмотра. Критерии select запроса:

        1. История не добавлена в таблицу Views => не просмотрена пользователем

        2. История является активной (не скрытой)

        Автоматически добавляет выбранную историю в таблицу Views
        :return:
        """
        v = list(map(lambda x: x.story.id, Views.select().where(Views.user == self.db_user)[:]))
        try:
            n: Stories = random.choice(Stories.select().where((~Stories.id.in_(v)) & Stories.is_active))
        except (IndexError, AttributeError):
            self.edit(PageLoader(16)().to_dict)
            return
        Views.create(user=self.db_user, story=n)
        n.author.stat.views += 1
        Stats.save(n.author.stat)

        pld = PageLoader(17)
        pld += [button('Оказать уважение', f'respect 1 {n.author.id}')]
        if self.db_user.is_admin:
            pld += [button('Скрыть историю', f'hide_story {n.id}')]
        self.edit(pld(
            n.title,
            n.author.author_name,
            n.text
        ).to_dict)

    @no_bug
    def hide_story(self, story_id):
        """
        Скрывает историю (Делает неактивной)
        :param story_id: ID истории
        :return:
        """
        try:
            strr = Stories.get_by_id(int(story_id))
            strr.is_active = False
            Stories.save(strr)
            self.edit(PageLoader(19)().to_dict)
            time.sleep(1)
            self.send(PageLoader(11)().to_dict)
        except Exception as e:
            print(e)
        self.next_story()

    @no_bug
    def clear_views(self):
        """
        Очищает таблицу Views для пользователя, отправившего запрос
        :return:
        """
        for v in Views.select().where(Views.user == self.db_user):
            try:
                Views.delete_by_id(v.id)
            except Exception as e:
                err = e
        self.edit(PageLoader(20)().to_dict)

    @no_bug
    def respect(self, amount, author_id):
        """
        Прибавляет уважение к автору с указанным ID
        :param amount: размер респекта
        :param author_id: ID автора кто получит респект
        :return:
        """
        try:
            ath = Authors.get_by_id(author_id)
            ath.stat.respect += int(amount)
            Stats.save(ath.stat)
            self.edit(PageLoader(18)(ath.author_name).to_dict)
            time.sleep(1)
        except Exception as e:
            print(e)
            error = e
        self.next_story()

    @no_bug
    def at_story(self, _id):
        """
        Высылает историю с указанным ID (Для inline поиска)
        :param _id: ID истории
        :return:
        """
        try:
            strr: Stories = Stories.get_by_id(_id)
            self.edit(PageLoader(17)(
                strr.title,
                strr.author.author_name,
                strr.text,
            ).to_dict)
        except Exception as e:
            err = e


class Search:
    def __init__(self, inline_query: InlineQuery):
        self.inline_query = inline_query
        self.query = inline_query.query
        self.s: bool = len(self.query) > 2

    def load_stories_by_text(self):
        return list(map(lambda x: InlineQueryResultArticle(x.id, x.title, InputTextMessageContent(f'/at_story {x.id}'), description=x.text[:128]), Stories.select().where((Stories.text.contains(self.query)) & Stories.is_active)[:15]))

    def load_stories_by_head(self):
        return list(map(lambda x: InlineQueryResultArticle(x.id, x.title, InputTextMessageContent(f'/at_story {x.id}'), description=x.text[:128]), Stories.select().where((Stories.title.contains(self.query)) & Stories.is_active)[:10]))

    def load_stories_by_author(self):
        return list(map(lambda x: InlineQueryResultArticle(x.id, x.title, InputTextMessageContent(f'/at_story {x.id}'), description=x.text[:128]), Stories.select().where((Stories.author.contains(Authors.select().where(Authors.author_name.contains(self.query)).limit(2))) & Stories.is_active)[:]))

    @staticmethod
    def uniq_id(answers):
        for a in zip(answers, range(1, len(answers) + 1)):
            a[0].id = a[1]
        return answers

    def search(self):
        if not self.s:
            return

        a = self.uniq_id([*self.load_stories_by_author(), *self.load_stories_by_head(), *self.load_stories_by_text()])
        GUARD.answer_inline_query(self.inline_query.id, a)
