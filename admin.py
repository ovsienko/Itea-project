from telebot import TeleBot
from config import SHOP_API_ADMIN
from models.models import Category, Additing
from bot.menus import *

bot = TeleBot(SHOP_API_ADMIN)


def add_category(message):
    add = Additing.objects.filter(tele_user = message.chat.id).first()
    if add.stage == 'start':
        bot.send_message(chat_id=message.chat.id, text='Мова категорії', reply_markup=lang_menu())
               add.stage = 'lang'
        add.save()
    elif add.stage == 'lang':
        if message.text == 'En' or message.text == 'Ua':
            add.category.lang = message.text
            add.category.save()
            add.stage = 'title'
            add.save()
            bot.send_message(chat_id=message.chat.id, text='Введіть назву категорії')
        else:
            bot.send_message(chat_id=message.chat.id, text='Мова категорії', reply_markup=lang_menu())
    elif add.stage == 'title':
        if len(message.text) > 3:
            add.category.title =  message.text
            add.category.save()
            add.stage = 'parent'
            add.save()
            bot.send_message(chat_id=message.chat.id, text='Це батьківська категорія?', reply_markup=parent_menu())
        else:
            bot.send_message(chat_id=message.chat.id, text='Введіть назву категорії')
    elif add.stage == 'parent':
        if message.text == 'Так':
            add.category.is_parent = True
            add.category.save()
            add.stage = 'sub'
            add.save()
            # TODO list category_list menu
        if message.text == 'Ні':
            add.category.is_parent = False
            add.category.save()
            add.delete()
            hello(message)
            #
        else:
            bot.send_message(chat_id=message.chat.id, text='Це батьківська категорія?', reply_markup=parent_menu())
        print(message)
@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(chat_id=message.chat.id, text='Моє шанування', reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    add = Additing.objects.filter(tele_user = message.chat.id).first()
    if add:
        add_category(message)
    else:
        hello(message)


    # bot.send_message(chat_id=message.chat.id, text='Моє шанування', reply_markup=main_menu())

@bot.callback_query_handler(func=lambda query: query.data == 'category_list')
def category_list(call):
    cats = Category.objects


@bot.callback_query_handler(func=lambda query: query.data == 'category_add')
def category_add(call):
    add = Additing.get_or_create(call.from_user.id)
    add_category(message=call.message)




if __name__ == '__main__':
    bot.polling()