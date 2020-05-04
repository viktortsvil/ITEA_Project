from web_shop.bot.setup import app, set_webhook, bot
from web_shop.db.seeder import seed
from web_shop.bot.config import DEBUG
#gunicorn --reload

if __name__ == '__main__':
    print(DEBUG)
    if not DEBUG:
        set_webhook()
        app.run(port=8000)
    else:
        seed()
        bot.polling()
