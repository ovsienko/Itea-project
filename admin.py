from telebot import TeleBot
from config import SHOP_API_ADMIN
from models.models import Category, AddCat, AddItem, Item
from bot.menus_admin import *

bot = TeleBot(SHOP_API_ADMIN)


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Моє шанування',
                     reply_markup=main_menu())

def add_category(message):
    add = AddCat.objects.filter(tele_user=message.chat.id).first()
    if add.stage == 'start':
        bot.send_message(chat_id=message.chat.id,
                         text='Введіть назву категорї')
        add.stage = 'title'
        add.save()
    elif add.stage == 'title':
        if len(message.text) > 3:
            add.category.title = message.text
            add.category.save()
            add.stage = 'en_title'
            add.save()
            bot.send_message(chat_id=message.chat.id,
                             text='Введіть назву категорії англійською')
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='Введіть назву категорії')
    elif add.stage == 'en_title':
        if len(message.text) > 3:
            add.category.title_en = message.text
            add.category.save()
            add.delete()
            bot.send_message(chat_id=message.chat.id,
                             text='Категорія збережена',
                             reply_markup=main_menu())
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='Введіть назву категорії англійською')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    add_cat = AddCat.objects.filter(tele_user=message.chat.id).first()
    add_itm = AddItem.objects.filter(tele_user=message.chat.id).first()
    if add_cat:
        add_category(message)
    elif add_itm:
        add_item(message)
    else:
        hello(message)


@bot.callback_query_handler(func=lambda query: query.data == 'category_list')
def category_list(call):
    print(call.message.chat.id)
    cats = Category.objects
    kl = category_list_menu(cats)
    bot.send_message(chat_id=call.message.chat.id,
                     text='Список категорій',
                     reply_markup=kl)


@bot.callback_query_handler(func=lambda
                            query: query.data.split('_')[0] == 'cat')
def category_more(call):
    cat = Category.objects.get(id=call.data.split('_')[1])
    ln = Item.objects.filter(category=cat).count()
    text = '''
    Назва категорії: {0}
    Назва категорії англійською: {1}
    Кількість товарів в категорії: {2}
    '''.format(cat.title, cat.title_en, ln)
    kb = cat_more_menu(cat)
    bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=kb)


# @bot.callback_query_handler(func=lambda
#                             query: query.data.split('_')[0] == 'catadd')


@bot.callback_query_handler(func=lambda
                            query: query.data == 'category_add')
def add_category_hand(call):
    AddCat.get_or_create(call.from_user.id)
    add_category(message=call.message)


@bot.callback_query_handler(func=lambda
                            query: query.data.split('_')[0] == 'catdel')
def category_delete(call):
    cat = Category.objects.get(id=call.data.split('_')[1])
    cat.delete_all()


def add_item(message):
    add = AddItem.objects.filter(tele_user=message.chat.id).first()
    if add.stage == 'start':
        add.stage = 'title'
        add.save()
        bot.send_message(chat_id=message.chat.id,
                         text='Введіть назву Товару')

    elif add.stage == 'title':
        if len(message.text) > 3:
            add.item.title = message.text
            add.item.save()
            add.stage = 'title_en'
            add.save()
            bot.send_message(chat_id=message.chat.id,
                             text='Введіть назву Товару англійською')
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='Введіть назву Товару')
    elif add.stage == 'title_en':
        if len(message.text) > 3:
            add.item.title_en = message.text
            add.item.save()
            add.stage = 'desc'
            add.save()
            bot.send_message(chat_id=message.chat.id,
                             text='Введіть опис товару')
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='ВВведіть назву Товару англійською')
    elif add.stage == 'desc':
        if len(message.text) > 3:
            add.item.desc = message.text
            add.item.save()
            add.stage = 'desc_en'
            add.save()
            bot.send_message(chat_id=message.chat.id,
                             text='Введіть опис товару англійською')
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='ВВведіть опис Товару')
    elif add.stage == 'desc_en':
        if len(message.text) > 3:
            add.item.desc_en = message.text
            add.item.save()
            add.stage = 'price'
            add.save()
            bot.send_message(chat_id=message.chat.id,
                             text='Введіть ціну товару в копійках')
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='ВВведіть опис Товару англійською')
    elif add.stage == 'price':
        try:
            prs = int(message.text)
            if prs > 0:
                print(prs)
                add.item.price = prs
                add.item.save()
                add.stage = 'quantity'
                add.save()
                bot.send_message(chat_id=message.chat.id,
                                 text='Введіть кількість товару')
            else:
                text = 'Введіть ціну товару в копійках більшу нуля'
                bot.send_message(chat_id=message.chat.id,
                                 text=text)
        except ValueError:
            bot.send_message(chat_id=message.chat.id,
                             text='Введіть ціну товару цифрами ')
    elif add.stage == 'quantity':
        try:
            qua = int(message.text)
            if qua >= 0:
                add.item.quantity = qua
                add.item.save()
                add.stage = 'photo'
                add.save()
                bot.send_message(chat_id=message.chat.id,
                                 text='Надішліть фото товару')
            else:
                bot.send_message(chat_id=message.chat.id,
                                 text='Кількість має бути більше або рівно 0')
        except ValueError:
            bot.send_message(chat_id=message.chat.id,
                             text='Введіть кількість товару цифрами ')
    elif add.stage == 'category':
        cat = Category.objects
        mark = category_list_item_menu(cat)
        bot.send_message(chat_id=message.chat.id,
                         text='Виберіть категорію товару', reply_markup=mark)


@bot.callback_query_handler(func=lambda
                            query: query.data == 'add_item')
def add_item_hand(call):
    AddItem.get_or_create(call.from_user.id)
    add_item(message=call.message)


@bot.message_handler(content_types='photo')
def image(message):
    add = AddItem.objects.filter(tele_user=message.chat.id).first()
    if add.stage == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        add.item.photo.put(downloaded_file, content_type='image/jpg')
        add.item.save()
        add.stage = 'category'
        add.save()
        add_item(message)


@bot.callback_query_handler(func=lambda
                            query: query.data == 'list_item')
def list_item(call):
    items = Item.objects
    mark = items_list_menu(items)
    bot.send_message(chat_id=call.message.chat.id,
                     text='Список товарів',
                     reply_markup=mark)


@bot.callback_query_handler(func=lambda
                            query: query.data.split('_')[0] == 'item')
def more_item(call):
    item = Item.objects.get(id=call.data.split('_')[1])
    bot.send_photo(call.message.chat.id, item.photo)
    msg = '''
    Назва: {0}
    Опис: {1}
    Ціна: {2}
    Кількість: {3}
    '''.format(item.title, item.desc, item.price, item.quantity)
    bot.send_message(chat_id=call.message.chat.id, text=msg)


@bot.callback_query_handler(func=lambda
                            query: query.data.split('_')[0] == 'itemcat')
def add_cat_to_item(call):
    add = AddItem.objects.get(tele_user=call.from_user.id)
    cat = Category.objects.get(id=call.data.split('_')[1])
    add.item.category = cat
    add.item.save()
    add.delete()
    hello(call.message)


if __name__ == '__main__':
    print('Admin bot is starting')
    bot.polling()
