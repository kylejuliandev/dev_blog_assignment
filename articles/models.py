import uuid
from django.conf import settings
from django.db import models

# Create your models here.
class Article(models.Model):
    """Represents an Article, found in the Article table"""
    id = models.UUIDField('article id', default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField('title', max_length=200)
    summary = models.CharField('summary', max_length=255)
    created_on = models.DateTimeField('article written on')
    updated_on = models.DateTimeField('article updated on')
    content = models.TextField('content')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)