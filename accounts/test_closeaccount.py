from django.test import TestCase
from accounts.models import User

class ManageTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        """Sets up test data, and creates a test user"""
        create_mock_user('TestUser', 'TestUser_P', False, True)
        return super().setUp()
    
    def tearDown(self) -> None:
        """Tears down test data, and removes all users"""
        User.objects.all().delete()
        return super().tearDown()
    
    def test_close_account_with_unauthenticated_user(self):
        """
            Given I am not authenticated,
            When I close my account,
            Then I am returned a 401 status
        """

        response = self.client.delete('/closeaccount')
        self.assertEqual(response.status_code, 401)

    def test_close_account_with_get_request(self): 
        """
            Given I am authenticated,
            When I close my account with a get request,
            Then I am returned a method not support status
        """

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.get('/closeaccount')
        self.assertEqual(response.status_code, 405)
    
    def test_close_account_with_post_request(self): 
        """
            Given I am authenticated,
            When I close my account with a post request,
            Then I am returned a method not support status
        """

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.post('/closeaccount')
        self.assertEqual(response.status_code, 405)
    
    def test_close_account_with_put_request(self): 
        """
            Given I am authenticated,
            When I close my account with a put request,
            Then I am returned a method not support status
        """

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.put('/closeaccount')
        self.assertEqual(response.status_code, 405)
    
    def test_close_anoynimises_pii(self): 
        """
            Given I am authenticated,
            When I close my account with a delete request,
            Then my user account is closed and pii data is anoynimised
        """

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.delete('/closeaccount')

        users = User.objects.all()
        user = users.first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.first_name, '[removed]')
        self.assertEqual(user.last_name, '[removed]')
        self.assertNotEqual(user.username, 'testuser')
        self.assertFalse(user.is_active)

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