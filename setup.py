from web_shop.bot.setup import app, set_webhook
from web_shop.db.seeder import generate

if __name__ == '__main__':
    set_webhook()
    generate(category=3, product=10, news=4)
    app.run(port=8000, debug=True)
