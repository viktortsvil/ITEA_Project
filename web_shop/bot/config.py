from ..log_writer import log_write

TOKEN = '1173186926:AAEDr0YjZBbgfWSrWSRd0EE3jz9CsxjJ0-8'
DEBUG = False


try:
    from .local_config import *
    log_write("Running in development mode")
except ImportError:
    log_write("Running in production mode")