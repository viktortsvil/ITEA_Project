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


def create_text(**kwargs):
    required_fields = ('text',)
    validated = [kwargs[arg] for arg in required_fields]
    return Texts.objects.create(**kwargs).save()


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


def generate(category=0, product=0, news=0):
    while category > 0:
        unique_arg = f"{random.randint(0, 10 ** 10)}"
        category_data = get_category_data(unique_arg)
        db_category = Category.objects.filter(slug=category_data['slug'])
        if db_category:
            continue

        print(f"Categories: {len(Category.objects)}")
        if len(Category.objects):
            make_it_subc = not random.randint(0, 2)
            if make_it_subc:
                print(f"Make it subc: True")
                parents = Category.objects
                parents_wo_products = [p for p in parents if len(p.products) == 0]
                parent = parents_wo_products[random.randint(0, len(parents_wo_products) - 1)]
                print(f"Categories without products: {len(parents_wo_products)}")
                category_data['parent'] = parent
                new_category = create_category(**category_data)
                parent.subcategories.append(new_category)
                parent.save()
            else:
                print(f"Make it subc: False")
                create_category(**category_data)
        else:
            create_category(**category_data)
        category -= 1
    while product > 0:
        unique_arg = f"{random.randint(0, 10 ** 10)}"
        product_data = get_product_data(unique_arg)
        categories = Category.objects.filter()
        leaf_categories = [c for c in categories if len(c.subcategories) == 0]
        category_ = leaf_categories[random.randint(0, len(leaf_categories) - 1)]
        product_data['category'] = category_
        db_product = Product.objects.filter(slug=product_data['slug'])
        if db_product:
            continue
        create_product(**product_data)
        product -= 1
    while news > 0:
        unique_arg = f"{random.randint(0, 10 ** 10)}"
        news_data = get_news_data(unique_arg)
        db_news = News.objects.filter(**news_data)
        if db_news:
            continue
        create_news(**news_data)
        news -= 1
    texts = ["Greeting"]
    for text in texts:
        text = {"text": text}
        text_db = Texts.objects.filter(**text)
        if text_db:
            continue
        create_text(**text)


def seed():
    a = input("Run seeder? Y/n")
    if a.lower() == 'y':
        print("Seeder running")
        generate(category=int(input("Categories: ")), product=int(input("Products: ")), news=int(input("News: ")))
