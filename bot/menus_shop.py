from telebot.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup,
                           KeyboardButton)
from models.models import Menu


def choose_lang():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='🇺🇦', callback_data='lang_🇺🇦'))
    kb.add(InlineKeyboardButton(text='🇺🇸', callback_data='lang_🇺🇸'))
    return kb


def main_menu(lang):
    kb = InlineKeyboardMarkup()
    btns = Menu.objects.filter(lang=lang, name='main')
    for btn in btns:
        print(btn.callb)
        kb.add(InlineKeyboardButton(text=btn.title, callback_data=btn.callb))
    return kb


def cats_list(cats, lang):
    kb = InlineKeyboardMarkup()
    for cat in cats:
        text = cat.get_card(lang)
        kb.add(InlineKeyboardButton(text=text,
                                    callback_data='items_' + str(cat.id)))
    return kb

