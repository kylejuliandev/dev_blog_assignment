from datetime import datetime
from django.test import TestCase
from accounts.models import User
from articles.models import Article, Comment
from articles.testhelpers import create_mock_admin, create_mock_author, create_mock_articles

class ArticleTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        author = create_mock_author('TestUser', 'TestUser_P')
        create_mock_author('AlternativeTestUser', 'AlternativeTestUser_P')
        create_mock_admin('AdminTestUser', 'AdminTestUser_P')
        create_mock_articles(author, 10)
        return super().setUp()
    
    def tearDown(self) -> None:
        User.objects.all().delete()
        Article.objects.all().delete()
        return super().tearDown()
    
    def test_article_get_with_no_article_id(self): 
        response = self.client.get('/article')

        self.assertEqual(response.status_code, 302)

    def test_article_get_with_no_comments(self):
        article_id = str(Article.objects.all().first().id)

        response = self.client.get('/article/' + article_id)

        self.assertEqual(response.status_code, 200)

    def test_article_get_with_comments(self):
        article = Article.objects.all().first()
        article_id = str(article.id)

        comment = Comment()
        comment.author = User.objects.all().first()
        comment.article = article
        comment.content = 'Great article!'
        comment.created_on = datetime.utcnow()
        comment.save()

        response = self.client.get('/article/' + article_id)

        self.assertEqual(response.status_code, 200)

    def test_article_delete_and_is_author(self):
        article = Article.objects.all().first()
        article_id = str(article.id)

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.post('/article/' + article_id)

        checkArticle = Article.objects.filter(id=article.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(checkArticle.count(), 0)

    def test_article_delete_and_is_not_author(self):
        article = Article.objects.all().first()
        article_id = str(article.id)

        self.client.login(username='alternativetestuser', password='AlternativeTestUser_P')
        response = self.client.post('/article/' + article_id)

        checkArticle = Article.objects.get(id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(checkArticle)
    
    def test_article_delete_and_is_admin(self):
        article = Article.objects.all().first()
        article_id = str(article.id)

        self.client.login(username='admintestuser', password='AdminTestUser_P')
        response = self.client.post('/article/' + article_id)

        checkArticle = Article.objects.filter(id=article.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(checkArticle.count(), 0)