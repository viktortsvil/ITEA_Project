from web_shop.bot.setup import app, set_webhook, bot
from web_shop.db.seeder import seed, generate
from web_shop.bot.config import DEBUG
from web_shop.db.models import is_db_empty
#gunicorn --reload

if __name__ == '__main__':
    if not DEBUG:
        if is_db_empty():
            generate(category=10, product=25, news=5)
        set_webhook()
        app.run(port=8000)
    else:
        seed()
        bot.polling()
