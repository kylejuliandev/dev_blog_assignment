import os

from dev_blog.settings.connection import connection

DEBUG = False
ALLOWED_HOSTS = [ 'kylejuliandevblog.herokuapp.com', 'localhost', '127.0.0.1', '[::1]', ]

databaseUrl = os.environ.get('DATABASE_URL')

if (databaseUrl):
    connectionDetails = connection.Connection.Map(databaseUrl)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': connectionDetails.Database,
            'USER': connectionDetails.Username,
            'PASSWORD': connectionDetails.Password,
            'HOST': connectionDetails.Host,
            'PORT': connectionDetails.Port
        }
    }

