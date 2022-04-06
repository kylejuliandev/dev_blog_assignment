from datetime import datetime
from uuid import uuid4
from django.test import TestCase
from accounts.models import User
from articles.models import Article, Comment
from articles.testhelpers import create_user, create_mock_article, create_mock_comment, get_random_string

class EditArticleTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        create_user('TestUser', 'TestUser_P', False, False)
        author = create_user('AuthorTestUser', 'AuthorTestUser_P', True, False)
        create_user('AdminTestUser', 'AdminTestUser_P', False, True)
        create_mock_article(author)

        return super().setUp()
    
    def tearDown(self) -> None:
        User.objects.all().delete()
        Article.objects.all().delete()
        return super().tearDown()
    
    def test_edit_article_get_as_unauthenticated(self):
        article = Article.objects.all().first()
        response = self.client.get('/article/' + str(article.id) + '/edit')

        self.assertEqual(response.status_code, 302)

    def test_edit_article_get_as_authenticated_but_not_original_author(self):
        article = Article.objects.all().first()

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.get('/article/' + str(article.id) + '/edit')

        self.assertEqual(response.status_code, 302)

    def test_edit_article_get_as_authenticated_as_original_author(self):
        article = Article.objects.all().first()

        self.client.login(username='authortestuser', password='AuthorTestUser_P')
        response = self.client.get('/article/' + str(article.id) + '/edit')

        checkArticle = Article.objects.get(id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkArticle.title, article.title)
        self.assertEqual(checkArticle.summary, article.summary)
        self.assertEqual(checkArticle.content, article.content)
        self.assertEqual(checkArticle.created_on, article.created_on)
        self.assertEqual(checkArticle.updated_on, article.updated_on)

    def test_edit_article_get_as_authenticated_as_admin(self):
        article = Article.objects.all().first()

        self.client.login(username='admintestuser', password='AdminTestUser_P')
        response = self.client.get('/article/' + str(article.id) + '/edit')

        checkArticle = Article.objects.get(id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkArticle.title, article.title)
        self.assertEqual(checkArticle.summary, article.summary)
        self.assertEqual(checkArticle.content, article.content)
        self.assertEqual(checkArticle.created_on, article.created_on)
        self.assertEqual(checkArticle.updated_on, article.updated_on)

        form = response.context['form']
        actual_title = str(form.fields['title'].initial)
        actual_summary = str(form.fields['summary'].initial)
        actual_content = str(form.fields['content'].initial)
        self.assertEqual(actual_title, article.title)
        self.assertEqual(actual_summary, article.summary)
        self.assertEqual(actual_content, article.content)

    def test_edit_article_get_with_missing_article(self):
        self.client.login(username='authortestuser', password='AuthorTestUser_P')
        response = self.client.get('/article/' + str(uuid4()) + '/edit')

        self.assertEqual(response.status_code, 302)

    def test_edit_article_get_with_missing_article_as_admin(self):
        self.client.login(username='admintestuser', password='AdminTestUser_P')
        response = self.client.get('/article/' + str(uuid4()) + '/edit')

        self.assertEqual(response.status_code, 302)

    def test_edit_article_with_title_too_long(self):
        article = Article.objects.all().first()
        title = get_random_string(201)
        data = {
            'title': title,
            'summary': 'New summary',
            'content': 'New content'
        }

        self.client.login(username='authortestuser', password='AuthorTestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/edit', data=data)

        checkArticle = Article.objects.get(id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(checkArticle.title, title)
        self.assertNotEqual(checkArticle.summary, 'New summary')
        self.assertNotEqual(checkArticle.content, 'New content')
        self.assertEqual(checkArticle.created_on, article.created_on)
        self.assertEqual(checkArticle.updated_on, article.updated_on)

    def test_edit_article_with_summary_too_long(self):
        article = Article.objects.all().first()
        summary = get_random_string(256)
        data = {
            'title': 'New title',
            'summary': summary,
            'content': 'New content'
        }

        self.client.login(username='authortestuser', password='AuthorTestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/edit', data=data)

        checkArticle = Article.objects.get(id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(checkArticle.title, 'New title')
        self.assertNotEqual(checkArticle.summary, summary)
        self.assertNotEqual(checkArticle.content, 'New content')
        self.assertEqual(checkArticle.created_on, article.created_on)
        self.assertEqual(checkArticle.updated_on, article.updated_on)

    def test_edit_article(self):
        article = Article.objects.all().first()
        data = {
            'title': 'New title',
            'summary': 'New summary',
            'content': 'New content'
        }

        self.client.login(username='authortestuser', password='AuthorTestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/edit', data=data)

        checkArticle = Article.objects.get(id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkArticle.title, 'New title')
        self.assertEqual(checkArticle.summary, 'New summary')
        self.assertEqual(checkArticle.content, 'New content')
        self.assertEqual(checkArticle.created_on, article.created_on)
        self.assertNotEqual(checkArticle.updated_on, article.updated_on)

    def test_edit_article_as_admin(self):
        article = Article.objects.all().first()
        data = {
            'title': 'New title',
            'summary': 'New summary',
            'content': 'New content'
        }

        self.client.login(username='admintestuser', password='AdminTestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/edit', data=data)

        checkArticle = Article.objects.get(id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkArticle.title, 'New title')
        self.assertEqual(checkArticle.summary, 'New summary')
        self.assertEqual(checkArticle.content, 'New content')
        self.assertEqual(checkArticle.created_on, article.created_on)
        self.assertNotEqual(checkArticle.updated_on, article.updated_on)