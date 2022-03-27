from django import forms
from django.contrib import admin

# Register your models here.
class PublishArticleForm(forms.Form):
    """Form to represent the creation of a article"""

    title = forms.CharField(label='title', max_length=200)
    summary = forms.CharField(label='summary', max_length=255, widget=forms.Textarea(attrs={'style':'height:100px;'}))
    content = forms.CharField(label='content', widget=forms.Textarea(attrs={'style':'height:200px;'}))