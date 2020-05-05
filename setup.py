from web_shop.bot.setup import app, set_webhook, bot
from web_shop.db.seeder import seed, generate
from web_shop.bot.config import DEBUG
from web_shop.db.models import is_db_empty
from web_shop.api.setup import start as startAPI
from web_shop.log_writer import log_write, log_clear
#gunicorn --reload

if __name__ == '__main__':
    log_clear()
    if is_db_empty():
        generate(category=10, product=25, news=5)
    if not DEBUG:
        startAPI()
        log_write("API STARTED SUCCESSFULLY")
        set_webhook()
        log_write("WEBHOOK SET SUCCESSFULLY")
        app.run(port=8000)
    else:
        startAPI()
        print("API STARTED SUCCESSFULLY")
        app.run(port=8000)
        bot.polling()
