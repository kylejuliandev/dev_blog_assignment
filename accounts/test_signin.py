from django.test import TestCase
from accounts.models import User

class LoginTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        """Sets up test data. Creates three users"""
        setup_active_test_user('ActiveTestUser', 'ActiveTestUser_P', False)
        setup_active_test_user('ActiveTestAuthor', 'ActiveTestAuthor_P', True)
        setup_inactive_test_user('InactiveTestUser', 'InactiveTestUser_P', False)
        return super().setUp()
    
    def tearDown(self) -> None:
        """Tears down test data, and removes all User objects"""
        User.objects.all().delete()
        return super().tearDown()

    def test_login_in_not_post(self):
        """
            Given I have no provided the username and password,
            When I login,
            I am redirected to the login page
        """

        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
    
    def test_login_in_with_active_user(self):
        """
            Given an active user exists,
            When I login with correct credentials,
            I am redirected to the home page and am logged in
        """

        response = self.client.post('/login', data={ 'username': 'ActiveTestUser', 'password': 'ActiveTestUser_P' })
        self.assertEqual(response.status_code, 302) # Redirected to home page
    
    def test_login_in_with_incorrect_password(self):
        """
            Given an active user exists,
            When I login a incorrect password,
            I am redirected to the login page and am not logged in
        """

        response = self.client.post('/login', data={ 'username': 'ActiveTestUser', 'password': 'wrong_password' })
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, 'User Id or Password was incorrect', html=True)
    
    def test_login_in_with_missing_username(self):
        """
            Given an active user exists,
            When I login a incorrect username,
            I am redirected to the login page and am not logged in
        """

        response = self.client.post('/login', data={ 'username': 'wrong_username', 'password': 'wrong_password' })
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, 'User Id or Password was incorrect', html=True)
    
    def test_login_in_with_to_in_active_account(self):
        """
            Given an inactive user exists,
            When I login,
            I am redirected to the login page and am not logged in
        """

        response = self.client.post('/login', data={ 'username': 'InactiveTestUser', 'password': 'InactiveTestUser_P' })
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, 'User Id or Password was incorrect', html=True)

def setup_active_test_user(username:str, password:str, isauthor:bool):
    """Create a active user"""
    create_mock_user(username, password, isauthor, True)

def setup_inactive_test_user(username:str, password:str, isauthor:bool):
    """Create a inactive user"""
    create_mock_user(username, password, isauthor, False)

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