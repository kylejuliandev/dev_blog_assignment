from datetime import datetime
from django.test import TestCase
from accounts.models import User
from articles.models import Article, Comment
from articles.testhelpers import create_mock_admin, create_mock_author, create_mock_articles

class ArticleTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        """Sets up test data for a run. Creates three users and 10 articles"""
        author = create_mock_author('TestUser', 'TestUser_P')
        create_mock_author('AlternativeTestUser', 'AlternativeTestUser_P')
        create_mock_admin('AdminTestUser', 'AdminTestUser_P')
        create_mock_articles(author, 10)
        return super().setUp()
    
    def tearDown(self) -> None:
        """Tears down test data that was created in a test run"""
        User.objects.all().delete()
        Article.objects.all().delete()
        return super().tearDown()
    
    def test_article_get_with_no_article_id(self): 
        """
            Given mock article has been created,
            When get article without specified id,
            Then I am redirected to the home page
        """
        response = self.client.get('/article')

        self.assertEqual(response.status_code, 302)

    def test_article_get_with_no_comments(self):
        """
            Given mock article has been created,
            When get article with specified id,
            Then I am shown the article
        """
        article_id = str(Article.objects.all().first().id)

        response = self.client.get('/article/' + article_id)

        self.assertEqual(response.status_code, 200)

    def test_article_get_with_comments(self):
        """
            Given mock article has been created with a single comment,
            When get article with specified id,
            Then I am shown the article with the comment
        """

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
        """
            Given mock article has been created,
            When I send a delete request as the author,
            Then the article is removed
        """

        article = Article.objects.all().first()
        article_id = str(article.id)

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.post('/article/' + article_id)

        checkArticle = Article.objects.filter(id=article.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(checkArticle.count(), 0)

    def test_article_delete_and_is_not_author(self):
        """
            Given mock article has been created,
            When I send a delete request as not the author,
            Then the article is not removed
        """

        article = Article.objects.all().first()
        article_id = str(article.id)

        self.client.login(username='alternativetestuser', password='AlternativeTestUser_P')
        response = self.client.post('/article/' + article_id)

        checkArticle = Article.objects.get(id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(checkArticle)
    
    def test_article_delete_and_is_admin(self):
        """
            Given mock article has been created,
            When I send a delete request as an admin,
            Then the article is removed
        """

        article = Article.objects.all().first()
        article_id = str(article.id)

        self.client.login(username='admintestuser', password='AdminTestUser_P')
        response = self.client.post('/article/' + article_id)

        checkArticle = Article.objects.filter(id=article.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(checkArticle.count(), 0)