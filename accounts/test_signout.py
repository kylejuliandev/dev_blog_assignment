from django.test import TestCase
from accounts.models import User

class SignoutTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        create_mock_user('TestUser', 'TestUser_P', False, True)
        return super().setUp()
    
    def tearDown(self) -> None:
        User.objects.all().delete()
        return super().tearDown()
    
    def test_signout(self):
        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.get('/logoff')
        self.assertEqual(response.status_code, 302) # Redirected to home page

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