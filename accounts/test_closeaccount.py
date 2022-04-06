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
    
    def test_close_account_with_unauthenticated_user(self):
        response = self.client.delete('/closeaccount')
        self.assertEqual(response.status_code, 401)

    def test_close_account_with_get_request(self): 
        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.get('/closeaccount')
        self.assertEqual(response.status_code, 405)
    
    def test_close_account_with_post_request(self): 
        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.post('/closeaccount')
        self.assertEqual(response.status_code, 405)
    
    def test_close_account_with_put_request(self): 
        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.put('/closeaccount')
        self.assertEqual(response.status_code, 405)
    
    def test_close_anoynimises_pii(self): 
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