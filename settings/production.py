from settings.base import *
from settings.db import DATABASES as db_prod_settings

DEBUG = False

DATABASES = db_prod_settings
