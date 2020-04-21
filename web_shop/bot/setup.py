from telebot import TeleBot, types
from .config import TOKEN
from ..db.models import Category, Texts, News, Product
from .keyboard import START_KB
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update)
from flask import Flask, request, abort

bot = TeleBot(TOKEN)

app = Flask.run(__name__)


@app.route('/', methods=['POST'])
def process_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(status=403)


@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [KeyboardButton(value) for value in START_KB.values()]
    kb.add(*buttons)

    # print(type(message))
    # kb = types.InlineKeyboardMarkup(row_width=2)
    # buttons = [types.InlineKeyboardButton(c.title, callback_data='category-'+c.slug) for c in Category.objects]
    # kb.add(*buttons)

    text = Texts.objects.filter(text='Greeting')[0].text
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=kb
    )


@bot.message_handler(func=lambda msg: msg.text == START_KB['categories'])
def get_categories(message):
    categories = Category.get_root()
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=category.title, callback_data=f"category-{category.id}") for category in
               categories]
    kb.add(*buttons)
    bot.send_message(
        chat_id=message.chat.id,
        text="Выберите Категорию",
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('category-'))
def category_handler(call):
    category_id = ''.join(call.data.split('-')[1::])
    category = Category.objects.get(id=category_id)
    if category.subcategories:
        kb = InlineKeyboardMarkup(row_width=2)
        buttons = []
        if category.parent:
            buttons += [InlineKeyboardButton(text='<- Back <-', callback_data=f"category-{category.parent.id}")]
        buttons += [InlineKeyboardButton(text=category.title, callback_data=f"category-{category.id}") for category in
                    category.subcategories]
        kb.add(*buttons)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            text=category.title,
            reply_markup=kb,
            message_id=call.message.message_id
        )
    else:
        for product in category.products:
            kb = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text="Add to Cart", callback_data=f"product-{product.id}")
            kb.add(button)
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=product.image.read(),
                caption=product.description,
                reply_markup=kb,
                disable_notification=True
            )


# @bot.callback_query_handler(func=lambda call: call.data.startswith('product-'))


@bot.message_handler(func=lambda msg: msg.text == START_KB['news'])
def get_news(message):
    news = News.objects.filter()
    kb = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text=i.title, callback_data=f"news-{i.id}") for i in news]
    kb.add(*buttons)
    bot.send_message(
        chat_id=message.chat.id,
        text=START_KB['news'],
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('news-'))
def get_certain_news(call):
    news_id = call.data.split('-')[-1]
    news = News.objects.get(id=news_id)
    bot.send_message(
        chat_id=call.from_user.id,
        text=f"{news.title}\n\n{news.body}"
    )


@bot.message_handler(func=lambda msg: msg.text == START_KB['discount_products'])
def get_discount_products(message):
    products = Product.get_discount_products()
    kb = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text=i.title, callback_data=f"product-{i.id}") for i in products]
    kb.add(*buttons)
    bot.send_message(
        chat_id=message.chat.id,
        text=START_KB['discount_products'],
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('product-'))
def get_certain_product(call):
    product_id = call.data.split('-')[-1]
    product = Product.objects.get(id=product_id)
    bot.send_message(
        chat_id=call.from_user.id,
        text=f"{product.title}\n\nPrice: {product.price}" +
             f"\nDiscount: {product.discount_percentage}%" if product.discount_percentage else f""
    )


def start_bot():
    print("Initializing the bot")
    bot.polling()


def set_webhook():
    import time
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(
        url='https://216.250.119.29/tg',
        certificate=open('web_cert.pem', 'r')
    )
