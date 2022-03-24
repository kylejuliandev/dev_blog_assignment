from django import forms

class LoginForm(forms.Form):
    email_address = forms.EmailField()
    password = forms.CharField()