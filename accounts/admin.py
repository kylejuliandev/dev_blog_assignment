from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from accounts.models import User

# Register your models here.
class LoginForm(forms.Form):
    """Form to represent the login page. User is expected to provide a Username and Password"""

    username = forms.CharField()
    password = forms.CharField()

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.lower()

class SignupForm(forms.Form):
    """Form to represent the sign up page. User is expected ot provide the base details, such as Username, First name and Last name.
    Additionally, the user will need to provide the password twice. They must be matching in order to proceed with the sign up process"""

    username = forms.CharField(label='username', max_length=255)
    first_name = forms.CharField(label='first name', max_length=50)
    last_name = forms.CharField(label='last name', max_length=50)
    password1 = forms.CharField(label='password1')
    password2 = forms.CharField(label='password2')

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.lower()

class ManageForm(forms.Form):
    """This form represents the form for managing an existing user account. You are permitted to change the first name and last name. In order for the changes to be persisted the user must also ensure their password is entered."""

    first_name = forms.CharField(label='first name', max_length=50)
    last_name = forms.CharField(label='last name', max_length=50)
    password = forms.CharField(label='password')

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password. This is used during the createsuperuser utilty process with django manage.py"""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_author', 'password1', 'password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user, but replaces the password field with admin's disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'is_author', 'is_active', 'is_admin')

class UserAdmin(BaseUserAdmin):
    """A user admin is a user with elevated permissions. They have the is_admin flag set to true. This gives them access to the django admin user interface."""

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'first_name', 'last_name', 'is_author', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'is_author',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'is_author', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name',)
    ordering = ('username', 'first_name', 'last_name',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)