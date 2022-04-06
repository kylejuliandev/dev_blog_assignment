import random
import string
from django.test import TestCase
from accounts.models import User

class ManageTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        create_mock_user('TestUser', 'TestUser_P', False, True)
        return super().setUp()
    
    def tearDown(self) -> None:
        User.objects.all().delete()
        return super().tearDown()
    
    def test_manage_not_post(self):
        user = User.objects.get(username='testuser')
        self.client.login(username='testuser', password='TestUser_P')

        response = self.client.get('/manage')
        
        form = response.context['form']
        actual_firstname = str(form.fields['first_name'].initial)
        actual_lastname = str(form.fields['last_name'].initial)
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(actual_firstname, user.first_name)
        self.assertEqual(actual_lastname, user.last_name)
    
    def test_manage_with_incorrect_password(self):
        self.client.login(username='testuser', password='TestUser_P')
        data = {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'password': 'incorrect_password'
        }

        response = self.client.post('/manage', data=data)
        
        user = User.objects.get(username='testuser')
        self.assertNotEqual(response.status_code, 302)
        self.assertNotEqual(user.first_name, 'NewFirstName')
        self.assertNotEqual(user.last_name, 'NewLastName')

    def test_manage_with_missing_password(self):
        self.client.login(username='testuser', password='TestUser_P')
        data = {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName'
        }

        response = self.client.post('/manage', data=data)
        
        user = User.objects.get(username='testuser')
        self.assertNotEqual(response.status_code, 302)
        self.assertNotEqual(user.first_name, 'NewFirstName')
        self.assertNotEqual(user.last_name, 'NewLastName')

    def test_manage_with_missing_first_name(self):
        self.client.login(username='testuser', password='TestUser_P')
        data = {
            'last_name': 'NewLastName',
            'password': 'TestUser_P'
        }

        response = self.client.post('/manage', data=data)
        
        user = User.objects.get(username='testuser')
        self.assertNotEqual(response.status_code, 302)
        self.assertNotEqual(user.last_name, 'NewLastName')

    def test_manage_with_missing_last_name(self):
        self.client.login(username='testuser', password='TestUser_P')
        data = {
            'first_name': 'NewFirstName',
            'password': 'TestUser_P'
        }

        response = self.client.post('/manage', data=data)
        
        user = User.objects.get(username='testuser')
        self.assertNotEqual(response.status_code, 302)
        self.assertNotEqual(user.first_name, 'NewFirstName')

    def test_manage_with_first_name_containing_numbers(self):
        self.client.login(username='testuser', password='TestUser_P')
        firstname = get_random_string_with_numbers(50)
        data = {
            'first_name': firstname,
            'last_name': 'NewLastName',
            'password': 'TestUser_P'
        }

        response = self.client.post('/manage', data=data)
        
        user = User.objects.get(username='testuser')
        self.assertNotEqual(response.status_code, 302)
        self.assertNotEqual(user.first_name, firstname)
        self.assertNotEqual(user.last_name, 'NewLastName')

    def test_manage_with_last_name_containing_numbers(self):
        self.client.login(username='testuser', password='TestUser_P')
        lastname = get_random_string_with_numbers(50)
        data = {
            'first_name': 'NewFirstName',
            'last_name': lastname,
            'password': 'TestUser_P'
        }

        response = self.client.post('/manage', data=data)
        
        user = User.objects.get(username='testuser')
        self.assertNotEqual(response.status_code, 302)
        self.assertNotEqual(user.first_name, 'NewFirstName')
        self.assertNotEqual(user.last_name, lastname)

    def test_manage_with_first_name_too_many_characters(self):
        self.client.login(username='testuser', password='TestUser_P')
        firstname = get_random_string(51)
        data = {
            'first_name': firstname,
            'last_name': 'NewLastName',
            'password': 'TestUser_P'
        }

        response = self.client.post('/manage', data=data)
        
        user = User.objects.get(username='testuser')
        self.assertNotEqual(response.status_code, 302)
        self.assertNotEqual(user.first_name, firstname)
        self.assertNotEqual(user.last_name, 'NewLastName')

    def test_manage_with_last_name_too_many_characters(self):
        self.client.login(username='testuser', password='TestUser_P')
        lastname = get_random_string(51)
        data = {
            'first_name': 'NewFirstName',
            'last_name': lastname,
            'password': 'TestUser_P'
        }

        response = self.client.post('/manage', data=data)
        
        user = User.objects.get(username='testuser')
        self.assertNotEqual(response.status_code, 302)
        self.assertNotEqual(user.first_name, 'NewFirstName')
        self.assertNotEqual(user.last_name, lastname)

    def test_manage_saves_changes(self):
        self.client.login(username='testuser', password='TestUser_P')
        data = {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'password': 'TestUser_P'
        }

        response = self.client.post('/manage', data=data)
        
        user = User.objects.get(username='testuser')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.first_name, 'NewFirstName')
        self.assertEqual(user.last_name, 'NewLastName')

    def test_manage_saves_partial_changes(self):
        self.client.login(username='testuser', password='TestUser_P')
        data = {
            'first_name': 'NewFirstName',
            'last_name': 'User',
            'password': 'TestUser_P'
        }

        response = self.client.post('/manage', data=data)
        
        user = User.objects.get(username='testuser')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.first_name, 'NewFirstName')
        self.assertEqual(user.last_name, 'User')

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