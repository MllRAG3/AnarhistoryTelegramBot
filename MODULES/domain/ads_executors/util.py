def extract_buttons(message):
    """
    :param message: Информация о сообщении, откуда надо извлечь кнопки
    :return: Словарь с информацией о кнопках
    """
    buttons = message.reply_markup
    if buttons:
        buttons = buttons.to_dict()
    return buttons
