from web_shop.bot.setup import app, set_webhook
from web_shop.db.seeder import generate

if __name__ == '__main__':
    set_webhook()
    category = int(input())
    product = int(input())
    news = int(input())
    generate(category=category, product=product, news=news)
    app.run(port=8000, debug=True)
