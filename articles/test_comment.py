from django.test import TestCase
from accounts.models import User
from articles.models import Article, Comment
from articles.testhelpers import create_mock_author, create_mock_articles, get_random_string

class CommentTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        """Sets up test data. Creates mock author and publishes 10 articles"""
        author = create_mock_author('TestUser', 'TestUser_P')
        create_mock_articles(author, 10)
        return super().setUp()
    
    def tearDown(self) -> None:
        """Tears down the created data. Removes all users and articles"""
        User.objects.all().delete()
        Article.objects.all().delete()
        return super().tearDown()
    
    def test_comment_not_authenticated(self):
        """
            Given article exists,
            When I try to comment and I am not authenticated,
            Then I an redirected to the home page
        """

        article_id = str(Article.objects.all().first().id)
        response = self.client.get('/article/' + article_id + '/comment')

        self.assertEqual(response.status_code, 302)

    def test_comment_get(self):
        """
            Given article exists,
            When I try to get comment and I am authenticated,
            Then I load the comment creation page
        """

        article = Article.objects.all().first()

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.get('/article/' + str(article.id) + '/comment')
        
        checkComment = Comment.objects.filter(article=article)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkComment.count(), 0)

    def test_comment_with_too_long_content(self):
        """
            Given article exists,
            When I try to comment with content that is too long,
            Then I am redirected to the article page and my comment is not added
        """

        article = Article.objects.all().first()
        data = {
            'content': get_random_string(281)
        }

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/comment', data=data)
        
        checkComment = Comment.objects.filter(article=article)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkComment.count(), 0)

    def test_comment(self):
        """
            Given article exists,
            When I try to comment with content that is too long,
            Then I am redirected to the article page and my comment is added
        """

        article = Article.objects.all().first()
        data = {
            'content': 'This is a great article!'
        }

        self.client.login(username='testuser', password='TestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/comment', data=data)
        
        checkComment = Comment.objects.filter(article=article)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkComment.count(), 1)