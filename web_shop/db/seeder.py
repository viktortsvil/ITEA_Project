from .models import (
    Category,
    Product,
    Texts,
    News,
    Characteristics,
    Customer
)
import random


def get_customer_data(unique_arg):
    pass


def get_characteristics_data(unique_arg):
    return {
        'height': random.randint(10, 200) / 10,
        'width': random.randint(10, 200) / 10,
        'weight': random.randint(10, 200)
    }


def get_category_data(unique_arg):
    return {
        'title': f'Category {unique_arg}',
        'slug': f'category-{unique_arg}',
        'description': f'Description of {unique_arg} category'
    }


def get_product_data(unique_arg):
    discount_percentage = random.randint(0, 1)
    if discount_percentage:
        discount_percentage = random.randint(1, 70)
    return {
        'title': f'Product {unique_arg}',
        'slug': f'product-{unique_arg}',
        'description': f'Description of {unique_arg} product',
        'price': random.randint(1, 50) * 100,
        'discount_percentage': discount_percentage
    }


def get_news_data(unique_arg):
    return {
        'title': f'News: {unique_arg}',
        'body': f'body-{unique_arg}',
    }


def create_customer(**kwargs):
    pass


def create_characteristics(**kwargs):
    pass


def create_category(**kwargs):
    required_fields = ('title', 'slug')
    validated = [kwargs[arg] for arg in required_fields]
    return Category.objects.create(**kwargs).save()


def create_product(**kwargs):
    required_fields = ('title', 'slug', 'price')
    validated = [kwargs[arg] for arg in required_fields]
    return Product.objects.create(**kwargs).save()


def create_news(**kwargs):
    required_fields = ('title', 'body')
    validated = [kwargs[arg] for arg in required_fields]
    return News.objects.create(**kwargs).save()


def generate(customers=0, characteristics=0, category=0, product=0, news=0):
    while customers > 0:
        print("Field customers is not implemented yet")
        customers -= 1
        break
    while characteristics > 0:
        characteristics -= 1
    while category > 0:
        unique_arg = f"{random.randint(0, 10**10)}"
        category_data = get_category_data(unique_arg)
        db_category = Category.objects.filter(slug=category_data['slug'])
        if db_category:
            continue
        create_category(**category_data)
        category -= 1
    while product > 0:
        unique_arg = f"{random.randint(0, 10**10)}"
        product_data = get_product_data(unique_arg)
        db_product = Product.objects.filter(slug=product_data['slug'])
        if db_product:
            continue
        create_product(**product_data)
        product -= 1
    while news > 0:
        unique_arg = f"{random.randint(0, 10**10)}"
        news_data = get_news_data(unique_arg)
        db_news = News.objects.filter(**news_data)
        if db_news:
            continue
        create_news(**news_data)
        news -= 1


if __name__ == '__main__':
    generate(category=5, product=10, news=5)
