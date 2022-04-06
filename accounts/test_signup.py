import random
import string
from django.test import TestCase

from accounts.models import User

class SignupTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        """Sets up test data"""
        return super().setUp()
    
    def tearDown(self) -> None:
        """Tears down test data, removes all user objects"""
        User.objects.all().delete()
        return super().tearDown()
    
    def test_signup_not_post(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
    
    def test_signup_with_no_username(self):
        """
            Given no username has been provided,
            When I sign up,
            I am redirected to signup page
        """

        data = {
            'password1': 'Password01',
            'password2': 'Password01',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)
    
    def test_signup_with_no_password(self):
        """
            Given no password has been provided,
            When I sign up,
            I am redirected to signup page
        """

        data = {
            'username': 'TestUser',
            'password2': 'Password01',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)

    def test_signup_with_no_confirmation_password(self):
        """
            Given no confirmation password has been provided,
            When I sign up,
            I am redirected to signup page
        """

        data = {
            'username': 'TestUser',
            'password1': 'Password01',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)

    def test_signup_with_no_first_name(self):
        """
            Given no first name has been provided,
            When I sign up,
            I am redirected to signup page
        """

        data = {
            'username': 'TestUser',
            'password1': 'Password01',
            'password2': 'Password01',
            'last_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)

    def test_signup_with_no_last_name(self):
        """
            Given no last name has been provided,
            When I sign up,
            I am redirected to signup page
        """

        data = {
            'username': 'TestUser',
            'password1': 'Password01',
            'password2': 'Password01',
            'first_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)

    def test_signup_with_password_is_too_short(self):
        """
            Given the password is too short,
            When I sign up,
            I am redirected to signup page and no user account is created
        """

        data = {
            'username': 'TestUser', 
            'password1': 'Pass',
            'password2': 'Pass',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, 'Password is too short', html=True)

    def test_signup_with_mismatching_passwords(self):
        """
            Given the password and confirmation password do not match,
            When I sign up,
            I am redirected to signup page and no user account is created
        """

        data = {
            'username': 'TestUser', 
            'password1': 'Password01',
            'password2': 'Password02',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, 'Passwords do not match', html=True)

    def test_signup_with_first_name_too_long(self):
        """
            Given the first name is too long,
            When I sign up,
            I am redirected to signup page and no user account is created
        """

        data = {
            'username': 'TestUser', 
            'password1': 'Password01',
            'password2': 'Password01',
            'first_name': get_random_string(51),
            'last_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)
    
    def test_signup_with_last_name_too_long(self):
        """
            Given the last name is too long,
            When I sign up,
            I am redirected to signup page and no user account is created
        """

        data = {
            'username': 'TestUser', 
            'password1': 'Password01',
            'password2': 'Password01',
            'first_name': 'Test',
            'last_name': get_random_string(51)
        }

        response = self.client.post('/signup', data)
        self.assertNotEqual(response.status_code, 302)

    def test_signup_with_first_name_containing_numbers(self):
        """
            Given the first name contains numbers,
            When I sign up,
            I am redirected to signup page and no user account is created
        """

        data = {
            'username': 'TestUser', 
            'password1': 'Password01',
            'password2': 'Password01',
            'first_name': get_random_string_with_numbers(50),
            'last_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, 'Name cannot only consist of letters', html=True)
    
    def test_signup_with_last_name_containing_numbers(self):
        """
            Given the last name contains numbers,
            When I sign up,
            I am redirected to signup page and no user account is created
        """

        data = {
            'username': 'TestUser', 
            'password1': 'Password01',
            'password2': 'Password01',
            'first_name': 'Test',
            'last_name': get_random_string_with_numbers(50)
        }

        response = self.client.post('/signup', data)
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, 'Name cannot only consist of letters', html=True)

    def test_signup_with_existing_username(self):
        """
            Given a user account exists with the username already,
            When I sign up,
            I am redirected to signup page and no user account is created
        """

        username = 'TestUser'
        create_mock_user(username, 'OtherUsersPassword', False, True)

        data = {
            'username': username, 
            'password1': 'Password01',
            'password2': 'Password01',
            'first_name': get_random_string(50),
            'last_name': get_random_string(50)
        }

        response = self.client.post('/signup', data)
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, 'Invalid username or password', html=True)
    
    def test_signup_successfully(self):
        """
            Given no user account exists with the username already,
            When I sign up,
            I am redirected to home page and a user account is created
        """

        firstname = get_random_string(50)
        lastname = get_random_string(50)
        data = {
            'username': 'TestUser', 
            'password1': 'Password01',
            'password2': 'Password01',
            'first_name': firstname,
            'last_name': lastname
        }

        response = self.client.post('/signup', data)
        user = User.objects.get(username='testuser')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.first_name, firstname)
        self.assertEqual(user.last_name, lastname)
        

def get_random_string(length:int) -> str:
    """Creates a random string from ascii letter characters"""
    return ''.join(random.choice(string.ascii_letters) for x in range(length))

def get_random_string_with_numbers(length:int) -> str:
    """Creates a random string from digits only"""
    return ''.join(random.choice(string.digits) for x in range(length))

def create_mock_user(username:str, password:str, isauthor:bool, isactive:bool):
    """Create a new user with the specified details"""
    user = User()
    user.username = username.lower()
    user.first_name = 'Test'
    user.last_name = 'User'
    user.is_author = isauthor
    user.is_active = isactive
    user.is_admin = False
    user.set_password(password)
    user.save()