import sys
import os
import os

sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = "settings.developing"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
