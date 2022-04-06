from datetime import datetime
from django.test import TestCase
from accounts.models import User
from articles.models import Article, Comment
from articles.testhelpers import create_user, create_mock_article, create_mock_comment, get_random_string

class PublishArticleTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        create_user('TestUser', 'TestUser_P', False, False)
        create_user('AuthorTestUser', 'AuthorTestUser_P', True, False)
        create_user('AdminTestUser', 'AdminTestUser_P', False, True)

        return super().setUp()
    
    def tearDown(self) -> None:
        User.objects.all().delete()
        Article.objects.all().delete()
        return super().tearDown()
    
    def test_publish_article_get_unauthenticated(self):
        response = self.client.get('/article')

        articles = Article.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(articles.count(), 0)

    def test_publish_article_get_authenticated_but_not_author_or_admin(self):
        self.client.login(username='testuser', password='TestUser_P')

        response = self.client.get('/article')

        articles = Article.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(articles.count(), 0)

    def test_publish_article_get_as_author(self):
        self.client.login(username='authortestuser', password='AuthorTestUser_P')

        response = self.client.get('/article')

        articles = Article.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(articles.count(), 0)

    def test_publish_article_get_as_admin(self):
        self.client.login(username='admintestuser', password='AdminTestUser_P')

        response = self.client.get('/article')

        articles = Article.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(articles.count(), 0)

    def test_publish_article_post_with_title_too_long(self):
        self.client.login(username='admintestuser', password='AdminTestUser_P')
        data = {
            'title': get_random_string(201),
            'summary': 'Test summary',
            'content': 'Test content'
        }

        response = self.client.post('/article', data=data)

        articles = Article.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(articles.count(), 0)

    def test_publish_article_post_with_summary_too_long(self):
        self.client.login(username='admintestuser', password='AdminTestUser_P')
        data = {
            'title': 'Test title',
            'summary': get_random_string(256),
            'content': 'Test content'
        }

        response = self.client.post('/article', data=data)

        articles = Article.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(articles.count(), 0)

    def test_publish_article_post(self):
        self.client.login(username='admintestuser', password='AdminTestUser_P')
        title = get_random_string(200)
        summary = get_random_string(255)
        data = {
            'title': title,
            'summary': summary,
            'content': 'Test content'
        }

        response = self.client.post('/article', data=data)

        articles = Article.objects.all()
        user = User.objects.get(username='admintestuser')
        article = articles.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(article.title, title)
        self.assertEqual(article.summary, summary)
        self.assertEqual(article.content, 'Test content')
        self.assertEqual(article.author, user)