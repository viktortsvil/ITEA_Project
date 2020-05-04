TOKEN = '1173186926:AAEDr0YjZBbgfWSrWSRd0EE3jz9CsxjJ0-8'
DEBUG = False


try:
    from .local_config import *
except ImportError:
    print("Running in production mode")