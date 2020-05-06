from flask_restful import Api
from web_shop.bot.setup import app
from .resources import CategoryResource, CartResource, CustomerResource, NewsResource, TextsResource, ProductResource


def start():
    api = Api(app)
    api.add_resource(CategoryResource, '/category', '/category/<category_id>')
    api.add_resource(CustomerResource, '/customer', '/customer/<customer_id>')
