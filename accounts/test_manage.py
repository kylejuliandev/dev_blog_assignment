import random
import string
from django.test import TestCase
from accounts.models import User

class ManageTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        """Creates test data and adds a uest user"""
        create_mock_user('TestUser', 'TestUser_P', False, True)
        return super().setUp()
    
    def tearDown(self) -> None:
        """Tears down test data and removes all test users"""
        User.objects.all().delete()
        return super().tearDown()
    
    def test_manage_not_post(self):
        """
            Given I am authenticated,
            When I manage my account,
            Then I am shown the manage page
        """

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
        """
            Given I specified the wrong password,
            When I manage my account,
            Then I am shown the manage page and my account changes were not saved
        """

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
        """
            Given I have not specified the password,
            When I manage my account,
            Then I am shown the manage page and my account changes were not saved
        """

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
        """
            Given I have not specified the first name,
            When I manage my account,
            Then I am shown the manage page and my account changes were not saved
        """

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
        """
            Given I have not specified the last name,
            When I manage my account,
            Then I am shown the manage page and my account changes were not saved
        """

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
        """
            Given I have specified a first name containing numbers,
            When I manage my account,
            Then I am shown the manage page and my account changes were not saved
        """

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
        """
            Given I have specified a last name containing numbers,
            When I manage my account,
            Then I am shown the manage page and my account changes were not saved
        """

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
        """
            Given I have specified a first name that is too long,
            When I manage my account,
            Then I am shown the manage page and my account changes were not saved
        """

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
        """
            Given I have specified a last name that is too long,
            When I manage my account,
            Then I am shown the manage page and my account changes were not saved
        """

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
        """
            Given a valid first and last name, and valid password,
            When I manage my account,
            Then I am redirected to the home page and my changes were saved
        """

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
        """
            Given that I only changed the last name,
            When I manage my account,
            Then I am redirected to the home page and my changes were saved
        """

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
    """Creates a random string from the ascii letter character set"""
    return ''.join(random.choice(string.ascii_letters) for x in range(length))

def get_random_string_with_numbers(length:int) -> str:
    """Creates a random string from digits"""
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