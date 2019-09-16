from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    main_kb = InlineKeyboardMarkup()
    main_kb.add(InlineKeyboardButton(text='Список категорій', callback_data='category_list'))
    main_kb.add(InlineKeyboardButton(text='Додати категорію', callback_data='category_add'))
    return main_kb

def parent_menu():
    markup = ReplyKeyboardMarkup()
    itembtna = KeyboardButton('Так')
    itembtnv = KeyboardButton('Ні')
    markup.row(itembtna, itembtnv)
    return markup

def lang_menu():
    markup = ReplyKeyboardMarkup()
    itembtna = KeyboardButton('En')
    itembtnv = KeyboardButton('Ua')
    markup.row(itembtna, itembtnv)
    return markup
