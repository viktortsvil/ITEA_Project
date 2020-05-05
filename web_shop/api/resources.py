from flask_restful import Resource
from flask import request, jsonify
import web_shop.db.models as m
import web_shop.api.schemas as s
from web_shop.log_writer import log_write


class CategoryResource(Resource):

    def get(self, category_id=None):
        response = None
        if category_id:
            try:
                category = m.Category.objects.get(id=category_id)
                response = s.CategorySchema().dump(category)
            except BaseException as e:
                log_write(f"Unsuccessful attempt to reach REST API -> 'category' with id {category_id}")
        else:
            categories = m.Category.objects
            response = s.CategorySchema().dump(categories, many=True)
        return jsonify(response)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class CustomerResource(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class CartResource(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class ProductResource(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class TextsResource(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class NewsResource(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
