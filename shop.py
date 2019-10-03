from telebot import TeleBot
from config import SHOP_API
from bot.menus_shop import *
from models.models import User, Text, Category, Item, Cart

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
    items = Item.objects.filter(category=cat)
    print(items)
    if not items:
        text = Text.objects.get(title='no_item', lang=user.lang).text
        bot.send_message(chat_id=call.message.chat.id,
                         text=text)
    else:
        for item in items:
            if user.lang == '🇺🇦':
                text = ''''
                    {0}
                    {1}
                    Ціна: {2}
                    Кількість: {3}
                '''.format(item.title, item.desc, item.price, item.quantity)
            else:
                text = ''''
                    {0}
                    {1}
                    Price: {2}
                    Quantity: {3}
                '''.format(item.title_en,
                           item.desc_en,
                           item.price,
                           item.quantity)
            mark = item_to_cart(item, user.lang)
            bot.send_photo(call.message.chat.id, item.photo)
            bot.send_message(chat_id=call.message.chat.id,
                             text=text,
                             reply_markup=mark,
                             parse_mode='HTML')


@bot.callback_query_handler(func=lambda
                            q: q.data.split('_')[0] == 'itemcart')
def add_to_cart(call):
    print('ttt')
    user = User.get_or_create_user(message=call)
    item = Item.objects.filter(id=call.data.split('_')[1]).first()
    Cart.create_or_append_to_cart(item, user)


@bot.callback_query_handler(func=lambda q: q.data == 'cart')
def cart(call):
    user = User.get_or_create_user(message=call)
    user_cart = Cart.objects.get(user=user)
    for item in user_cart.items:
        bot.send_message(chat_id=call.message.chat.id,
                         text=(item.title, item.price))
    text = 'Сума: ' + str(user_cart.get_sum)
    bot.send_message(chat_id=call.message.chat.id,
                     text=text)


if __name__ == '__main__':
    print('bot is starting')
    bot.polling()
