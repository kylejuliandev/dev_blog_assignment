DEBUG = True
ALLOWED_HOSTS = [ 'localhost', '127.0.0.1', '[::1]', ]

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