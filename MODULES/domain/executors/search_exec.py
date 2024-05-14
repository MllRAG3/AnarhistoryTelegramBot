# from telebot.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
# from MODULES.domain.pre_send.call_data_handler import Call
# from MODULES.constants.reg_variables.BOT import GUARD
# from MODULES.database.models.users import User
# from MODULES.database.models.stories import Story
#
#
# class SearchExecutor(Call):
#     def __init__(self, user):
#         self.tg_user = user
#         self.db_user: User = User.get_or_none(tg_id=self.tg_user.id)
#
#     def inline_mode_search(self, inline_query: InlineQuery):
#         if self.db_user is None:
#             GUARD.answer_inline_query(inline_query.id, [InlineQueryResultArticle(1, 'ВЫ НЕ ЗАРЕГЕСТРИРОВАНЫ! Нажмите, чтобы зарегистрироваться', InputTextMessageContent('/reg'))])
#             return
#         # in = .in_(value) or [field] << [value]  (<< - __lshift__, >> - __rshift__)
#         stories = Story.select().where((Story.in_review == 0) & (Story.title.contains(inline_query.query))).order_by(Story.rating.desc())[:self.db_user.search_preferensies.show_stories_in_inline_mode_n]
#         inline_answer = list(map(lambda x: InlineQueryResultArticle(x.id, x.title, InputTextMessageContent(f'/at_story {x.id}')), stories))
#         print(stories, inline_answer)
#         GUARD.answer_inline_query(inline_query.id, inline_answer)
