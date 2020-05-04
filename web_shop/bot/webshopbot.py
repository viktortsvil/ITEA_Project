from telebot import TeleBot
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update)

from typing import List, Union


class WebShopBot(TeleBot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate_inline_keyboard(self, buttons: List[InlineKeyboardButton], row_width=3):
        kb = InlineKeyboardMarkup(row_width=row_width)
        kb.add(*buttons)
        return kb

    def generate_reply_keyboard(self, buttons: List[KeyboardButton]):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(*buttons)
        return kb

    def send_message_or_photo(self, chat_id: int, text: str,
                              kb: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup] = None,
                              photo_bytes=None
                              ):
        if photo_bytes:
            self.send_photo(chat_id=chat_id, caption=text, photo=photo_bytes, reply_markup=kb)
        else:
            self.send_message(chat_id=chat_id, text=text, reply_markup=kb)

    def edit_message(self, chat_id: int, text: str, message_id: int,
                     kb: Union[InlineKeyboardMarkup] = None
                     ):
        self.edit_message_text(chat_id=chat_id, text=text, reply_markup=kb, message_id=message_id)

    def load_products(self, products, chat_id):
        for product in products:
            buttons = [InlineKeyboardButton(text="Add to Cart", callback_data=f"product-{product.id}")]
            self.send_message_or_photo(chat_id, product.description, self.generate_inline_keyboard(buttons),
                                       product.image.read() if product.image else None)

    def load_subcategories(self, category, chat_id, message_id):
        buttons = []
        if category.parent:
            buttons += [InlineKeyboardButton(text='<- Back <-', callback_data=f"category-{category.parent.id}")]
        buttons += [InlineKeyboardButton(text=category.title, callback_data=f"category-{category.id}") for category in
                    category.subcategories]
        self.edit_message(chat_id, category.title, message_id,
                          self.generate_inline_keyboard(buttons, row_width=2))

    def load_category_products(self, category, chat_id):
        self.load_products(category.products, chat_id)

    def generate_cart_message_data(self, cart):
        text = "Your cart:\n"
        total = 0
        buttons = []
        for item in cart.cart_items:
            text += f"{item.product.title} - {item.count}\n"
            total += item.product.price * item.count
            buttons += [InlineKeyboardButton(text='-', callback_data=f"minus-{item.product.id}"),
                        InlineKeyboardButton(text=f'{item.product.title}', callback_data="unreal_data"),
                        InlineKeyboardButton(text='+', callback_data=f"plus-{item.product.id}")]
        text += f"Total cost: {total}"
        buttons += [InlineKeyboardButton(text="Order", callback_data='order-goods')]
        kb = self.generate_inline_keyboard(buttons)
        return text, kb

    def load_cart_data(self, customer, chat_id):
        cart = customer.get_or_create_current_cart()[1]
        text, kb = self.generate_cart_message_data(cart)
        self.send_message_or_photo(chat_id, text, kb)

    def update_cart_data(self, customer, chat_id, message_id):
        cart = customer.get_or_create_current_cart()[1]
        text, kb = self.generate_cart_message_data(cart)
        self.edit_message(chat_id, text, message_id, kb)

    def add_product_to_cart(self, product_id, customer):
        cart = customer.get_or_create_current_cart()[1]
        for item in cart.cart_items:
            if str(item.product.id) == product_id:
                item.count += 1
                break
        cart.save()

    def remove_product_from_cart(self, product_id, customer):
        cart = customer.get_or_create_current_cart()[1]
        pop = None
        for i, item in enumerate(cart.cart_items):
            if str(item.product.id) == product_id:
                item.count -= 1
                if item.count == 0:
                    pop = i
                break
        if pop:
            cart.cart_items.pop(pop)
        cart.save()
