import json

import telebot.apihelper

from MODULES.constants.reg_variables.BOT import GUARD
from telebot.types import InlineKeyboardButton


def button(text, call_data) -> InlineKeyboardButton:
    return InlineKeyboardButton(text, callback_data=call_data)


def send(chat_id, type, kwargs_json, markup, **additional_buttons: list[InlineKeyboardButton]):
    kwargs = json.loads(kwargs_json)
    for row in additional_buttons.values():
        markup.row(row)

    match type:
        case 'text':
            GUARD.send_message(chat_id=chat_id, **kwargs, reply_markup=markup)
        case 'photo':
            GUARD.send_photo(chat_id=chat_id, **kwargs, reply_markup=markup)
        case 'audio':
            GUARD.send_audio(chat_id=chat_id, **kwargs, reply_markup=markup)
        case 'document':
            GUARD.send_document(chat_id=chat_id, **kwargs, reply_markup=markup)
        case 'video':
            GUARD.send_video(chat_id=chat_id, **kwargs, reply_markup=markup)
        case 'animation':
            GUARD.send_animation(chat_id=chat_id, **kwargs, reply_markup=markup)
        case _:
            raise NotImplementedError(f'Тип сообщений >>{type}<< не может быть отправлен данным методом!')


def safe_edit(func):
    def inner(mid, chat_id, *args, **kwargs):
        try:
            func(mid, chat_id, *args, **kwargs)
        except telebot.apihelper.ApiTelegramException:
            send(chat_id, 'text', ..., ...,)
            func(mid+1, chat_id, *args, **kwargs)

    return inner


@safe_edit
def edit(message_id, chat_id, type, kwargs_json, markup, **additional_buttons: list[InlineKeyboardButton]):
    kwargs = json.loads(kwargs_json)
    for row in additional_buttons.values():
        markup.row(row)

    match type:
        case 'text':
            GUARD.edit_message_text(message_id=message_id, chat_id=chat_id, **kwargs, reply_markup=markup)
        case _ as case if case in ['photo', 'audio', 'document', 'video', 'animation']:
            GUARD.edit_message_media(message_id=message_id, chat_id=chat_id, **kwargs)
            GUARD.edit_message_caption(message_id=message_id, chat_id=chat_id, **kwargs, reply_markup=markup)
        case _:
            raise NotImplementedError(f'Тип сообщений >>{type}<< не может быть отправлен данным методом!')
