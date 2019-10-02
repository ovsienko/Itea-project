from telebot.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup,
                           KeyboardButton)

from models.models import Item


def main_menu():
    main_kb = InlineKeyboardMarkup()
    main_kb.add(InlineKeyboardButton(text='Список категорій',
                                     callback_data='category_list'))
    main_kb.add(InlineKeyboardButton(text='Додати категорію',
                                     callback_data='category_add'))
    main_kb.add(InlineKeyboardButton(text='Додати товар',
                                     callback_data='add_item'))
    main_kb.add(InlineKeyboardButton(text='Cписок товарів',
                                     callback_data='list_item'))
    return main_kb


def category_list_menu(cats):
    kl = InlineKeyboardMarkup()
    for cat in cats:
        ln = Item.objects.filter(category=cat).count()
        title = '{0} ({1})'.format(cat.title, str(ln))
        kl.add(InlineKeyboardButton(text=title,
                                    callback_data='cat_' + str(cat.id)))
    return kl


def add_category_list_menu(cats):
    kl = InlineKeyboardMarkup()
    for cat in cats:
        kl.add(InlineKeyboardButton(text=cat.title,
                                    callback_data='catadd_' + str(cat.id)))
    return kl


def category_list_item_menu(cats):
    kl = InlineKeyboardMarkup()
    for cat in cats:
        kl.add(InlineKeyboardButton(text=cat.title,
                                    callback_data='itemcat_' + str(cat.id)))
    return kl


def cat_more_menu(cat):
    kl = InlineKeyboardMarkup()
    kl.add(InlineKeyboardButton(text='Видалити категорію',
                                callback_data='catdel_' + str(cat.id)))
    kl.add(InlineKeyboardButton(text='До списку категорій',
                                callback_data='category_list'))
    return kl


def items_list_menu(items):
    kl = InlineKeyboardMarkup()
    for i in items:
        kl.add(InlineKeyboardButton(text=i.title,
                                    callback_data='item_' + str(i.id)))
    return kl

