import mongoengine as me
import datetime
from typing import Tuple

#me.connect('SHOP_DB')
me.connect('SHOP_DB_TEST')

ValidationError = me.ValidationError
NotUniqueError = me.NotUniqueError
OperationError = me.OperationError
DoesNotExist = me.DoesNotExist

class Customer(me.Document):
    user_id = me.IntField(unique=True)
    username = me.StringField(min_length=1, max_length=256)
    phone_number = me.StringField()
    address = me.StringField()
    name = me.StringField(min_length=1, max_length=256)
    surname = me.StringField(min_length=1, max_length=256)
    age = me.IntField(min_value=1, max_value=99)
    is_blocked = me.BooleanField(default=False)

    def get_or_create_current_cart(self) -> Tuple[bool, 'Cart']:
        created = False
        cart = Cart.objects.filter(customer=self, is_archived=False)
        if cart:
            return created, cart[0]
        else:
            created = True
            cart = Cart.objects.create(customer=self).save()
            return created, cart

    def get_history(self):
        pass


class CartItem(me.EmbeddedDocument):
    product = me.ReferenceField('Product')
    count = me.IntField(default=1, min_value=1)

    @property
    def get_price(self):
        return self.product.get_price * self.count

    def __eq__(self, other):
        return self.product == other.product

    def __hash__(self):
        return hash(self.product)


class Cart(me.Document):
    customer = me.ReferenceField('Customer')
    cart_items = me.EmbeddedDocumentListField('CartItem')
    is_archived = me.BooleanField(default=False)

    def add_item(self, product):
        item = CartItem(product=product)
        if item in self.cart_items:
            self.cart_items[self.cart_items.index(item)].count += 1
        else:
            self.cart_items.append(item)
        self.save()

    def archive(self):
        self.is_archived = True
        self.save()


class Characteristics(me.EmbeddedDocument):
    height = me.DecimalField()
    width = me.DecimalField()
    weight = me.DecimalField()


class Category(me.Document):
    title = me.StringField(required=True, min_length=2, max_length=512)
    slug = me.StringField(required=True, min_length=2, max_length=512, unique=True)
    description = me.StringField(max_length=2048)
    subcategories = me.ListField(me.ReferenceField('self'))
    parent = me.ReferenceField('self')

    def add_subcategory(self, subc):
        subc.parent = self
        self.subcategories.append(subc.save())
        self.save()

    @classmethod
    def get_root(cls):
        return cls.objects(parent=None)

    @property
    def is_root(self):
        return self.parent is None

    @property
    def is_leaf(self):
        return not self.subcategories

    @property
    def products(self):
        return Product.objects(category=self)

    def __str__(self):
        return f"{self.title}\n" \
               f"{self.description}\n" \
               f"{self.parent}"


class Product(me.Document):
    title = me.StringField(required=True, min_length=2, max_length=512)
    slug = me.StringField(required=True, min_length=2, max_length=512, unique=True)
    description = me.StringField(min_length=2, max_length=2048)
    characteristics = me.EmbeddedDocumentField(Characteristics)
    price = me.DecimalField(required=True, min_value=0, force_string=True)
    discount_percentage = me.IntField(min_value=0, max_value=100, default=0)
    category = me.ReferenceField(Category)
    image = me.FileField()

    @classmethod
    def get_discount_products(cls):
        return cls.objects.filter(discount_percentage__gt=0)  # discount_percentage > 0

    def get_price(self):
        return self.price * (100 - self.discount_percentage) / 100


class News(me.Document):
    title = me.StringField(min_length=2, max_length=512)
    body = me.StringField(min_length=10, max_length=4096)
    pub_date = me.DateTimeField(default=datetime.datetime.utcnow)


class Texts(me.Document):
    choices = (
        ('Greeting', 'Greeting'),
        ('Buy', 'Buy')
    )
    text = me.StringField(choices=choices)

    def __str__(self):
        return self.text


def is_db_empty():
    result = False
    try:
        ctg = Category.objects
        if len(ctg) == 0:
            result = True
    finally:
        return result
