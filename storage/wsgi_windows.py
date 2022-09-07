import os
import sys
import site
from django.core.wsgi import get_wsgi_application
# Add the app’s directory to the PYTHONPATH
sys.path.append("D:\zander")
sys.path.append("D:\zander\storage")
os.environ['DJANGO_SETTINGS_MODULE'] = 'storage.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'storage.settings')
application=get_wsgi_application()
