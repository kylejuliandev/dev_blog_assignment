"""
WSGI config for dev_blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

env = os.environ.get('ENVIRONMENT')

if (env == 'prod'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev_blog.prod_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev_blog.settings')

application = get_wsgi_application()
