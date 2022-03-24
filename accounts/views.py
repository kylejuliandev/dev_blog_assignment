from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.admin import LoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout

import re

from accounts.models import User, UserManager

# Create your views here.
def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = str(form.cleaned_data['username'])
            passw = str(form.cleaned_data['password'])
            user = authenticate(username=user, password=passw)
            if user is not None:
                if user.is_active:
                    login(request=request, user=user)
                    return redirect(reverse(viewname='home'))
                else:
                    form.add_error(field=None, error='User account is locked')
            else:
                form.add_error(field=None, error='User Id or Password was incorrect')
    else:
        form = LoginForm()

    return render(request, 'accounts/signin.html', { 'form': form })

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            username = str(form.cleaned_data['username'])
            password1 = str(form.cleaned_data['password1'])
            password2 = str(form.cleaned_data['password2'])
            first_name = str(form.cleaned_data['first_name'])
            last_name = str(form.cleaned_data['last_name'])

            charactersOnlyPattern = '^[a-zA-Z]+$'

            if len(password1) < 8:
                form.add_error(field='password1', error='Password is too short')

            if password1 != password2:
                form.add_error(field='password2', error='Passwords do not match')
            
            if len(first_name) > 50:
                form.add_error(field='first_name', error='First name is too long')

            if len(last_name) > 50:
                form.add_error(field='last_name', error='Last name is too long')

            if not re.match(charactersOnlyPattern, first_name):
                form.add_error(field='first_name', error='First name cannot only consist of letters')

            if not re.match(charactersOnlyPattern, last_name):
                form.add_error(field='last_name', error='Last name cannot only consist of letters')
            
            if User.objects.filter(username=username).exists():
                form.add_error(field=None, error='Invalid username or password')
                return render(request, 'accounts/signup.html', { 'form': form })

            usermanager = UserManager()
            usermanager.model = User

            user = usermanager.create_user(
                username=username.lower(),
                first_name=first_name,
                last_name=last_name,
                is_author=False,
                password=password1)
            
            login(request=request, user=user)
            return redirect(reverse(viewname='home'))
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', { 'form': form })

def signout(request):
    logout(request)
    return redirect(reverse(viewname='home'))