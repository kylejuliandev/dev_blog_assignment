from django.shortcuts import redirect, render
from django.urls import reverse

from authentication.forms import LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def signin(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['email_address']
            passw = form.cleaned_data['password']
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

    return render(request, 'authentication/signin.html', { 'form': form })

def signout(request):
    logout(request)
    return redirect(reverse(viewname='home'))