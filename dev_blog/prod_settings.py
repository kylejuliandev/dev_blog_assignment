import os
from settings import *
from connection import Connection

DEBUG = False

databaseUrl = os.environ.get('DATABASE_URL')

if (databaseUrl):
    connectionDetails = Connection.Map(databaseUrl)

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