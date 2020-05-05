from web_shop.bot.setup import app, set_webhook, bot
from web_shop.db.seeder import seed, generate
from web_shop.bot.config import DEBUG
from web_shop.db.models import is_db_empty
from web_shop.api.setup import start as startAPI
#gunicorn --reload

if __name__ == '__main__':
    if is_db_empty():
        generate(category=10, product=25, news=5)
    if not DEBUG:
        startAPI()
        set_webhook()
        app.run(host="216.250.119.29", port=8000)
    else:
        startAPI()
        print("API STARTED SUCCESSFULLY")
        app.run(port=8000)
        bot.polling()
