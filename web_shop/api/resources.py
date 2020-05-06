from flask_restful import Resource
from flask import request, jsonify
import web_shop.db.models as m
from web_shop.api import schemas as s
from web_shop.log_writer import log_write


class GlobalResource:

    @staticmethod
    def get(model, schema, name, param):
        if param is not None:
            try:
                obj = model.objects.get(id=param)
                result = schema().dump(obj)
                log_write(f"Successful attempt to reach REST API GET -> '{name}' with id {param}")
            except (s.ValidationError, m.ValidationError, m.DoesNotExist) as e:
                log_write(
                    f"Unsuccessful attempt to reach REST API GET -> '{name}' with id {param}. Error: {str(e)}")
                result = str(e)
        else:
            objs = model.objects
            try:
                result = schema().dump(objs, many=True)
                log_write(f"Successful attempt to reach REST API GET -> '{name}'")
            except s.ValidationError as e:
                log_write(f"Unsuccessful attempt to reach REST API GET -> '{name}'. Error: {str(e)}")
                result = str(e)
        return jsonify(result)

    @staticmethod
    def post(model, schema, name):
        try:
            json = schema().load(request.get_json())
            result = schema().dump(model.objects.create(**json))
            log_write(f"Successful attempt to reach REST API POST -> '{name}'")
        except (s.ValidationError, m.NotUniqueError) as e:
            log_write(f"Unsuccessful attempt to reach REST API POST -> '{name}'. Error: {str(e)}")
            result = str(e)
        return jsonify(result)

    @staticmethod
    def put(model, schema, name, param):
        try:
            obj = model.objects.get(id=param)
            json: dict = schema().dump(obj)
            json.update(request.get_json())

            njson = {}
            for key, value in json.items():
                if json[key]:
                    njson[key] = value
            json = njson

            json = schema().load(json)
            obj.update(**json)
            obj.reload()
            result = schema().dump(obj)
            log_write(f"Successful attempt to reach REST API PUT -> '{name}' with id {param}")
        except (s.ValidationError, m.ValidationError, m.NotUniqueError, m.DoesNotExist) as e:
            log_write(
                f"Unsuccessful attempt to reach REST API PUT -> '{name}' with id {param}. Error: {str(e)}")
            result = str(e)
        return jsonify(result)

    @staticmethod
    def delete(model, name, param):
        if param:
            try:
                obj = model.objects.get(id=param)
                obj.delete()
                result = {'status': 'OK'}
            except (m.OperationError, m.ValidationError, m.DoesNotExist) as e:
                log_write(
                    f"Unsuccessful attempt to reach REST API DELETE -> '{name}' with id {param}. Error: {str(e)}")
                result = str(e)
        else:
            log_write(
                f"Unsuccessful attempt to reach REST API DELETE -> '{name}'. Error: parameter 'id' not specified!")
            result = {'status': 'Error'}
        return jsonify(result)




class CategoryResource(Resource):

    def get(self, category_id=None):
        return GlobalResource.get(m.Category, s.CategorySchema, 'category', category_id)
        if category_id:
            try:
                category = m.Category.objects.get(id=category_id)
                result = s.CategorySchema().dump(category)
                log_write(f"Successful attempt to reach REST API GET -> 'category' with id {category_id}")
            except (s.ValidationError, m.ValidationError, m.DoesNotExist) as e:
                log_write(
                    f"Unsuccessful attempt to reach REST API GET -> 'category' with id {category_id}. Error: {str(e)}")
                result = str(e)
        else:
            categories = m.Category.objects
            try:
                result = s.CategorySchema().dump(categories, many=True)
                log_write(f"Successful attempt to reach REST API GET -> 'category'")
            except s.ValidationError as e:
                log_write(f"Unsuccessful attempt to reach REST API GET -> 'category'. Error: {str(e)}")
                result = str(e)
        return jsonify(result)

    def post(self):
        return GlobalResource.post(m.Category, s.CategorySchema, 'category')
        try:
            category = s.CategorySchema().load(request.get_json())
            result = s.CategorySchema().dump(m.Category.objects.create(**category))
            log_write(f"Successful attempt to reach REST API POST -> 'category'")
        except (s.ValidationError, m.NotUniqueError) as e:
            log_write(f"Unsuccessful attempt to reach REST API POST -> 'category'. Error: {str(e)}")
            result = str(e)
        return jsonify(result)

    def put(self, category_id=None):
        return GlobalResource.put(m.Category, s.CategorySchema, 'category', category_id)
        try:
            category = m.Category.objects.get(id=category_id)
            json: dict = s.CategorySchema().dump(category)
            json.update(request.get_json())

            njson = {}
            for key, value in json.items():
                if json[key]:
                    njson[key] = value
            json = njson

            json = s.CategorySchema().load(json)
            category.update(**json)
            category.reload()
            result = s.CategorySchema().dump(category)
            log_write(f"Successful attempt to reach REST API PUT -> 'category' with id {category_id}")
        except (s.ValidationError, m.ValidationError, m.NotUniqueError, m.DoesNotExist) as e:
            log_write(
                f"Unsuccessful attempt to reach REST API PUT -> 'category' with id {category_id}. Error: {str(e)}")
            result = str(e)
        return jsonify(result)

    def delete(self, category_id=None):
        return GlobalResource.delete(m.Category, 'category', category_id)
        if category_id:
            try:
                category = m.Category.objects.get(id=category_id)
                category.delete()
                result = {'status': 'OK'}
            except (m.OperationError, m.ValidationError, m.DoesNotExist) as e:
                log_write(
                    f"Unsuccessful attempt to reach REST API DELETE -> 'category' with id {category_id}. Error: {str(e)}")
                result = str(e)
        else:
            log_write(
                f"Unsuccessful attempt to reach REST API DELETE -> 'category'. Error: parameter 'id' not specified!")
            result = {'status': 'Error'}
        return jsonify(result)


class CustomerResource(Resource):

    def get(self, customer_id=None):
        return GlobalResource.get(m.Customer, s.CustomerSchema, 'category', customer_id)

    def post(self):
        return GlobalResource.post(m.Customer, s.CustomerSchema, 'customer')

    def put(self, customer_id=None):
        return GlobalResource.put(m.Customer, s.CustomerSchema, 'category', customer_id)

    def delete(self, customer_id=None):
        return GlobalResource.delete(m.Customer, 'category', customer_id)


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
