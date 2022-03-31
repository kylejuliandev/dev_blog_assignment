from uuid import uuid4
from django.http import HttpResponse
from accounts.admin import LoginForm, ManageForm, SignupForm
from accounts.models import User, UserManager
from django.contrib.auth import authenticate, login, logout
from django.forms import Form
from django.shortcuts import redirect, render
from django.urls import reverse

import re
import hashlib

import logging

logger = logging.getLogger(__name__)

def signin(request):
    """User is presented with login form 'accounts/signin.html'"""

    if request.method != 'POST':
        form = LoginForm()
        return render(request, 'accounts/signin.html', { 'form': form })

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

    return render(request, 'accounts/signin.html', { 'form': form })

def signup(request):
    """Allows the user to sign up as a non-admin and non-author. User is presented with 'accounts/signup.html'"""

    if request.method != 'POST': 
        form = SignupForm()
        return render(request, 'accounts/signup.html', { 'form': form })

    form = SignupForm(request.POST)
    if form.is_valid():
        username = str(form.cleaned_data['username'])
        password1 = str(form.cleaned_data['password1'])
        password2 = str(form.cleaned_data['password2'])
        first_name = str(form.cleaned_data['first_name'])
        last_name = str(form.cleaned_data['last_name'])
        
        validate_password(form, password1, password2)
        validate_name(form, 'first_name', first_name)
        validate_name(form, 'last_name', last_name)
        
        if form.errors:
            logger.debug('User tried to sign up but the additional form validation failed')
            return render(request, 'accounts/signup.html', { 'form': form })

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
        
        # Set login authentication cookies
        login(request=request, user=user)
        return redirect(reverse(viewname='home'))
    else:
        logger.debug('User tried to sign up but the form validation failed')

    return render(request, 'accounts/signup.html', { 'form': form })

def signout(request):
    """Allows the users to logout of the platform. Removes any authentication cookies"""

    logout(request)
    return redirect(reverse(viewname='home'))

def manage(request):
    """Allows the users to configure user account details. Only supports first and last name."""

    user = request.user
    if not request.user.is_authenticated:
        return redirect(reverse(viewname='home'))

    if request.method != 'POST':
        form = ManageForm()
        form.fields['first_name'].initial = user.first_name
        form.fields['last_name'].initial = user.last_name
        return render(request, 'accounts/manage.html', { 'form': form })

    form = ManageForm(request.POST)
    if form.is_valid():
        # We need to authenticate that the user making the changes
        # owns the account
        passw = str(form.cleaned_data['password'])
        reauthenticatedUser = authenticate(username=user, password=passw)

        if reauthenticatedUser is None:
            form.add_error(field=None, error='User Id or Password was incorrect')
            return render(request, 'accounts/manage.html', { 'form': form })

        firstname = str(form.cleaned_data['first_name'])
        lastname = str(form.cleaned_data['last_name'])

        validate_name(form, 'first_name', firstname)
        validate_name(form, 'last_name', lastname)

        if not form.errors:
            reauthenticatedUser.first_name = firstname
            reauthenticatedUser.last_name = lastname

            try:
                logger.debug('Saving User %s details', user.username)
                reauthenticatedUser.save()
            except:
                logger.exception('Unable to update User %s details', user.username)

            return redirect(reverse(viewname='home'))
        else:
            logger.debug('User %s could not update their user details as additional form validation failed', user.username)
    else:
        logger.debug('User %s could not update their user details as form validation failed', user.username)

    return render(request, 'accounts/manage.html', { 'form': form })

def closeaccount(request):
    """Request a user deletion. User can only delete themselves. Django admin tool can be used to delete other users. We do not delete the record in the data, as to preserve database integrity. Instead we anonymise the data."""
    
    response = HttpResponse()
    user = request.user
    if not user.user.is_authenticated:
        response.status_code = 401
        return response
    
    if request.method != 'DELETE':
        response.status_code = 405
        return response

    user.first_name = "[removed]"
    user.last_name = "[removed]"

    uuid = uuid4()
    usernameAndUuid = str(user.username) + str(uuid)
    user.username = hashlib.sha256(usernameAndUuid.encode()).hexdigest()
    user.is_active = False

    try:
        logger.debug('Closing User %s account', user.username)
        user.save()
    except:
        logger.exception('Unable to close User %s account', user.username)

    # Remove auth cookies
    logout(request)
    
    response.status_code = 200
    return response

def validate_name(form:Form, field:str, input:str):
    """Validates a name field aganist pre-defined rules. Specifically that a name cannot be more than 50 characters long and 
    must consist of letters only. Adds a field specific error to the form."""

    # Only alphabetical characters are allowable
    charactersOnlyPattern = '^[a-zA-Z]+$'
    if len(input) > 50:
        form.add_error(field=field, error='Name is too long')
    
    if not re.match(charactersOnlyPattern, input):
        form.add_error(field=field, error='Name cannot only consist of letters')

def validate_password(form:Form, password1:str, password2:str):
    """Validates that two passwords are equal and that a password must be longer than 8 characters. Adds a field specific error to the form."""

    if len(password1) < 8:
        form.add_error(field='password1', error='Password is too short')

    if password1 != password2:
        form.add_error(field='password2', error='Passwords do not match')