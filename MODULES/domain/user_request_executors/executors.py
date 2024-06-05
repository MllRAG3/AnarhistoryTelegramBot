import json
import random
import time

from telebot.types import \
    Message, \
    User, \
    InlineQuery, \
    InlineQueryResultArticle, \
    InputTextMessageContent, \
    InlineKeyboardMarkup
from telebot.apihelper import ApiTelegramException

from MODULES.constants.reg_variables.BOT import GUARD
from MODULES.constants.reg_variables.MORPH import MORPH

from MODULES.domain.ads_executors.to_json import ToJson
from MODULES.domain.pre_send.call_data_handler import Call
from MODULES.domain.pre_send.page_compiler import PageLoader
from MODULES.domain.user_request_executors.graph_loader import Graph
from MODULES.domain.ads_executors.boost_counter import Boost
import MODULES.domain.user_request_executors.util as util


from MODULES.database.models.users import Authors, Stats
from MODULES.database.models.stories import Stories, Views
from peewee import DoesNotExist


from MODULES.constants.config import MAIN_BOT_TOKEN


def no_bug(func):
    """
    При возникновении ошибки в процессе выполнения метода
    высылает сообщение с соответствующим текстом
    :param func: Метод, который передается в декоратор
    :return:
    """
    def inner(self, *args, **kwargs):
        func(self, *args, **kwargs)
        # try:
        #     return func(self, *args, **kwargs)
        # except Exception as e:
        #     self.send(PageLoader(11)(f"({func.__name__}): {e}").to_dict)

    return inner


class Exec(Call):
    def __init__(self, message: Message, user: User | None = None):
        """
        :param message: Объект класса telebot.types.Message - информация о сообщении
        (для получения чата, пользователя и др.)
        :param user: Объект класса telebot.types.User - дополнительно информация о пользователе
        (актуально, когда в аргументе message содержится некорректная информация о пользователе)
        """
        self.message: Message = message
        self.user = message.from_user if user is None else user
        self.db_user: Authors | None = None

        self.load_db_user()

    def check_boosts(self):
        boost = Boost(self.db_user)
        if boost.boost_changed == 0:
            return
        elif boost.boost_changed < 0:
            self.boost_up(boost)
        elif boost.boost_changed > 0:
            self.boost_down(boost)

        boost.rollback()

    @no_bug
    def boost_up(self, bst):
        if not bst.chn_buttons:
            self.send(PageLoader(20)(-bst.boost_changed, -bst.boost_changed, ".").to_dict)
            return

        pld = PageLoader(20)
        for btn in bst.chn_buttons:
            pld += [btn]
        self.send(pld(-bst.boost_changed, -bst.boost_changed, ", но ты все еще можешь повысить его подписавшись на каналы ниже!").to_dict)

    @no_bug
    def boost_down(self, bst):
        if not bst.chn_buttons:
            return

        pld = PageLoader(21)
        for btn in bst.chn_buttons:
            pld += [btn]
        self.send(pld(bst.boost_changed, bst.boost_changed).to_dict)

    def send(self, data, chat_id=None):
        util.send(self.message.chat.id if chat_id is None else chat_id, **data)

    def edit(self, data):
        util.edit(self.message.id, self.message.chat.id, **data)

    @no_bug
    def load_db_user(self):
        """
        Загружает пользователя из базы данных;
        В случае отсутствия пользователя - создает запись
        :return:
        """
        try:
            self.db_user = Authors.get(tg_id=self.user.id)
        except DoesNotExist:
            stat = Stats.create()
            data = {
                'tg_id': self.user.id,
                'chat_id': self.message.chat.id,
                'username': self.user.username,
                'stat': stat
            }
            self.db_user = Authors.create(**data)

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

    def dismember_message(self):
        if not self.db_user.is_admin:
            return
        self.send(PageLoader(17)().to_dict)
        tj = ToJson()
        GUARD.register_next_step_handler(self.message, callback=tj)
        while not tj.is_called:
            pass
        self.send(PageLoader(18)(*tj.jresults).to_dict)

    def rickroll(self):
        self.send(PageLoader(19)().to_dict)

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
        tj = ToJson()
        GUARD.register_next_step_handler(self.message, callback=tj)
        while not tj.is_called:
            pass

        story_type, story_json, _ = tj.jresults
        GUARD.delete_message(self.message.chat.id, tj.message.id)
        if self.plagiat(tj.message.text if tj.message.text is not None else tj.message.caption):
            self.edit(PageLoader(13)().to_dict)
            return

        Stories.create(
            author=self.db_user,
            json=story_json,
            type=story_type,
        )

        self.edit(PageLoader(15)().to_dict)

    @no_bug
    def plagiat(self, text: str) -> bool:
        stories_texts = map(lambda x: json.loads(x.json), Stories.select())
        stories_texts = map(lambda x: x['text'] if 'text' in x.keys() else x['caption'], stories_texts)
        text = set(map(lambda y: MORPH.parse(util.remove_punctuation(y).lower())[0].normal_form, text.split()))
        stories_texts = list(map(lambda x: set(map(lambda y: MORPH.parse(util.remove_punctuation(y).lower())[0].normal_form, x.split())), stories_texts))

        pld = PageLoader(14)
        grp = Graph(len(stories_texts))

        for stext in stories_texts:
            if len(text & stext) / len(text) > 0.9:
                return True

            grp += 1
            self.edit(pld(str(grp)).to_dict)

        return False

    @no_bug
    def read_stories(self):
        """
        Высылает новую историю из бд для просмотра. Критерии select запроса:

        1. История не добавлена в таблицу Views => не просмотрена пользователем

        2. История является активной (не скрытой)

        Автоматически добавляет выбранную историю в таблицу Views
        :return:
        """
        v = list(map(lambda x: x.story.id, Views.select().where(Views.user == self.db_user)[:]))
        try:
            story: Stories = random.choice(Stories.select().where(~Stories.id.in_(v)))
        except (IndexError, AttributeError) as e:
            print(e)
            self.edit(PageLoader(16)().to_dict)
            return
        Views.create(user=self.db_user, story=story)
        story.author.stat.views += 1
        Stats.save(story.author.stat)

        markup = InlineKeyboardMarkup().row(
            util.button('👍', f'respect 1 {story.author.id}'),
            util.button('>>-ДАЛЬШЕ->', 'read_stories')
        )
        D = {'type': story.type, 'kwargs_json': story.json, 'markup': markup}
        self.edit(D)

    @no_bug
    def clear_views(self):
        """
        Очищает таблицу Views для пользователя, отправившего запрос
        :return:
        """
        for v in Views.select().where(Views.user == self.db_user):
            try:
                Views.delete_by_id(v.id)
            except ApiTelegramException:
                pass
        self.edit(PageLoader(16)().to_dict)

    @no_bug
    def respect(self, amount, author_id):
        """
        Прибавляет уважение к автору с указанным ID
        :param amount: размер респекта
        :param author_id: ID автора кто получит респект
        :return:
        """
        ath = Authors.get_by_id(author_id)
        ath.stat.respect += int(amount)
        Stats.save(ath.stat)
        self.edit(PageLoader(22)(ath.author_name, amount).to_dict)
        time.sleep(1)
        self.read_stories()

    @no_bug
    def at_story(self, id_):
        story: Stories = Stories.get_by_id(id_)
        D = {'type': story.type, 'kwargs_json': story.json}
        self.send(D)


class Search:
    """
    Класс для поиска по inline_query запросам от пользователя (telebot.types.InlineQuery)
    """
    def __init__(self, inline_query: InlineQuery, default_min=1, select_size=20):
        """
        :param inline_query: Объект класса telebot.types.InlineQuery - запрос от пользователя
        :param default_min: Минимальная длина текста запроса (если запрос меньше - поиск не осуществляется)
        :param select_size: Кол-во записей, которые будут отправлены ответом на запрос
        """
        self.inline_query = inline_query
        self.query = inline_query.query
        self.select_size = select_size
        self.s: bool = len(self.query) >= default_min

    def __call__(self):
        """
        Обращается к таблице Stories, выбирает записи (self.select_size)**, где:
        1.
          Заголовок содержит текст запроса*
        2.
          Текст содержит текст запроса*
        3.
          Все истории от автора (2)**, псевдоним которого содержит текст запроса*

        * передается при инициализации данного класса, (telebot.types.InlineQuery)
        ** Кол-во выбираемых записей
        :return: список с ответами на запрос inline_query
        """
        authors = Authors.select().where(Authors.author_name.contains(self.query)).limit(2)
        select = Stories\
            .select()\
            .where(
                (Stories.json.contains(self.query)) |
                (Stories.author.in_(authors))
            )\
            .limit(self.select_size)

        articles = []
        for res in select:
            D = json.loads(res.json)
            text = D['text'] if 'text' in D.keys() else D['caption']

            # if res.type in ['animation', 'photo', 'video']:
            #     path = GUARD.get_file(D[res.type]).file_path
            #     thumbnail = f"https://t.me/file/bot{MAIN_BOT_TOKEN}/{path}"
            # else:
            #     thumbnail = None

            articles.append(InlineQueryResultArticle(
                id=res.id,
                title=text + ('...' if len(text) > 32 else ''),
                input_message_content=InputTextMessageContent(f'/at_story {res.id}'),
                description=f"АВТОР: {res.author.author_name}\nТЕКСТ: {text[:128] + ('...' if len(text) > 128 else '')}",
            ))

        return articles

    def search(self):
        """
        Осуществляет поиск по переданному при инициализации inline_query (telebot.types.InlineQuery);

        Отвечает на запрос от пользователя при условии, что текст запроса длиннее переданного
        при инициализации (default_min (по умл. = 1))
        :return:
        """
        if not self.s:
            return

        GUARD.answer_inline_query(self.inline_query.id, self())
