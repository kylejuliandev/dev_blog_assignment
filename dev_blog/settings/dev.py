DEBUG = True
ALLOWED_HOSTS = [ 'localhost', '127.0.0.1', '[::1]', ]
SECRET_KEY = 'django-insecure-0c74$5oyu#y31t64vbcdp3z&3v6oee1a83f$w28y$_w+=9f&cn'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dev_blog',
        'USER': 'dev_blog_user',
        'PASSWORD': 'dev_blog_user_p',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}