import os
import sys	
sys.path.append('/home/www/book-genie.co/book_genie_site/book_genie')
os.environ['DJANGO_SETTINGS_MODULE'] = 'book_genie.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()