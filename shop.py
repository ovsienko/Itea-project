from telebot import TeleBot
from config import SHOP_API
from bot.menus_shop import *
from models.models import User, Text, Category, Item

bot = TeleBot(SHOP_API)


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Виберіть мову! Choose your language! ',
                     reply_markup=choose_lang())
    User.get_or_create_user(message=message)


@bot.callback_query_handler(func=lambda q: q.data.split('_')[0] == 'lang')
def set_lang(call):
    user = User.get_or_create_user(message=call)
    user.lang = call.data.split('_')[1]
    user.save()
    # print(user.lang)
    text = Text.objects.get(lang=user.lang, title='Greetings').text
    mark = main_menu(user.lang)
    bot.send_message(chat_id=call.message.chat.id,
                     text=text,
                     reply_markup=mark)


@bot.callback_query_handler(func=lambda q: q.data == 'news')
def get_news(call):
    user = User.get_or_create_user(message=call)
    news = Text.objects.get(title='news', lang=user.lang).text
    mark = main_menu(user.lang)
    bot.send_message(chat_id=call.message.chat.id,
                     text=news,
                     reply_markup=mark)


@bot.callback_query_handler(func=lambda q: q.data == 'info')
def get_info(call):
    user = User.get_or_create_user(message=call)
    info = Text.objects.get(title='info', lang=user.lang).text
    mark = main_menu(user.lang)
    bot.send_message(chat_id=call.message.chat.id,
                     text=info,
                     reply_markup=mark)


@bot.callback_query_handler(func=lambda q: q.data == 'cats')
def get_cats(call):
    user = User.get_or_create_user(message=call)
    cats = Category.objects
    bot.send_message(chat_id=call.message.chat.id,
                     text=Text.objects.get(title='cat_list',
                                           lang=user.lang).text,
                     reply_markup=cats_list(cats, user.lang))


@bot.callback_query_handler(func=lambda
                            q: q.data.split('_')[0] == 'items')
def items(call):
    user = User.get_or_create_user(message=call)
    cat = Category.objects.get(id=call.data.split('_')[1])
    items = Item.objects.filter(category=cat, lang=user.lang)
    for item in items:
        bot.send_message(chat_id=call.message.chat.id,
                         text=item.title)
        bot.send_photo(call.message.chat.id, item.photo_file)


if __name__ == '__main__':
    print('bot is starting')
    bot.polling()
