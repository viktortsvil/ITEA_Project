from web_shop.bot.setup import app, set_webhook, bot
from web_shop.db.seeder import seed, generate
from web_shop.bot.config import DEBUG
from web_shop.db.models import is_db_empty
from web_shop.api.setup import start as startAPI
from web_shop.log_writer import log_write, log_clear


log_clear()
log_write("STARTING LOGGING..")
if is_db_empty():
    generate(category=10, product=25, news=5)
if not DEBUG:
    log_write("STARTING API")
    startAPI()
    log_write("API STARTED SUCCESSFULLY")
    set_webhook()
    log_write("WEBHOOK SET SUCCESSFULLY")
    log_write("STARTING SERVER")
    app.run(port=8000)
else:
    startAPI()
    log_write("API STARTED SUCCESSFULLY")
    app.run(port=8000)
    bot.polling()
