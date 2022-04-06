from datetime import datetime
from django.test import TestCase
from accounts.models import User
from articles.models import Article, Comment
from articles.testhelpers import create_mock_admin, create_mock_author, create_mock_articles, get_random_string

class CommentTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        author = create_mock_author('TestUser', 'TestUser_P')
        create_mock_articles(author, 10)
        return super().setUp()
    
    def tearDown(self) -> None:
        User.objects.all().delete()
        Article.objects.all().delete()
        return super().tearDown()
    
    def test_comment_not_authenticated(self):
        article_id = str(Article.objects.all().first().id)
        response = self.client.get('/article/' + article_id + '/comment')

        self.assertEqual(response.status_code, 302)

    def test_comment_get(self):
        article_id = str(Article.objects.all().first().id)

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.get('/article/' + article_id + '/comment')
        
        self.assertEqual(response.status_code, 200)

    def test_comment_with_too_long_content(self):
        article = Article.objects.all().first()
        data = {
            'content': get_random_string(281)
        }

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/comment', data=data)
        
        checkArticle = Comment.objects.filter(article=article)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkArticle.count(), 0)

    def test_comment(self):
        article = Article.objects.all().first()
        data = {
            'content': 'This is a great article!'
        }

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/comment', data=data)
        
        checkArticle = Comment.objects.filter(article=article)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkArticle.count(), 1)