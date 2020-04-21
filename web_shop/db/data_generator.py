from .models import Category, Texts


def _generate_category(title: str,
                       description: str,
                       subcategories=None,
                       parent=None):
    slug = title.lower().replace(' ', '-')
    print(Category.objects.create(
        title=title,
        slug=slug,
        description=description,
        subcategories=subcategories,
        parent=parent
    ).save())


def add_text(text: str):
    print(Texts.objects.create(
        text=text
    ).save())


def add_category():
    while True:
        title = input("Name: ")
        description = input("Description: ")
        _generate_category(title, description)
