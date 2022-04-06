import random
import string
from django.test import TestCase

from accounts.models import User

class SignupTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        User.objects.all().delete()
        return super().tearDown()
    
    def test_signup_not_post(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
    
    def test_signup_with_no_username(self):
        data = {
            'password1': 'Password01',
            'password2': 'Password01',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)
    
    def test_signup_with_no_password(self):
        data = {
            'username': 'TestUser',
            'password2': 'Password01',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)

    def test_signup_with_no_confirmation_password(self):
        data = {
            'username': 'TestUser',
            'password1': 'Password01',
            'first_name': 'Test',
            'last_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)

    def test_signup_with_no_first_name(self):
        data = {
            'username': 'TestUser',
            'password1': 'Password01',
            'password2': 'Password01',
            'last_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)

    def test_signup_with_no_last_name(self):
        data = {
            'username': 'TestUser',
            'password1': 'Password01',
            'password2': 'Password01',
            'first_name': 'User'
        }

        response = self.client.post('/signup', data=data)
        self.assertNotEqual(response.status_code, 302)

    def test_signup_with_password_is_too_short(self):
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
    return ''.join(random.choice(string.ascii_letters) for x in range(length))

def get_random_string_with_numbers(length:int) -> str:
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