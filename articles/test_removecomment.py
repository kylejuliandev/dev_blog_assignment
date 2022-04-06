from django.test import TestCase
from accounts.models import User
from articles.models import Article, Comment
from articles.testhelpers import create_user, create_mock_article, create_mock_comment

class RemoveCommentTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        """Creates test data. Setups four users, a mock article and comment"""
        commentAuthor = create_user('CommentTestUser', 'CommentTestUser_P', False, False)
        create_user('OtherTestUser', 'OtherTestUser_P', False, False)
        create_user('AdminTestUser', 'AdminTestUser_P', False, True)
        articleAuthor = create_user('ArticleAuthorTestUser', 'ArticleAuthorTestUser_P', True, False)
        article = create_mock_article(articleAuthor)
        create_mock_comment(commentAuthor, article)

        return super().setUp()
    
    def tearDown(self) -> None:
        """Tears down test data. Specifically, it removes all user and article objects"""
        User.objects.all().delete()
        Article.objects.all().delete()
        return super().tearDown()
    
    def test_remove_comment_not_authenticated(self):
        """
            Given I am not authenticated and a comment exists,
            When I try to remove the comment,
            Then I am redirected to the home page and the comment is not removed
        """

        article = Article.objects.all().first()
        comment = Comment.objects.filter(article=article).first()
        
        response = self.client.post('/article/' + str(article.id) + '/comment/' + str(comment.id) +'/delete')

        checkComment = Comment.objects.filter(id=comment.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(checkComment.count(), 1)

    def test_remove_comment_authenticated_but_not_author(self):
        """
            Given a comment exists but I am not the author,
            When I try to remove the comment,
            Then I am redirected to the home page and the comment is not removed
        """

        article = Article.objects.all().first()
        comment = Comment.objects.filter(article=article).first()
        
        self.client.login(username='othertestuser', password='OtherTestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/comment/' + str(comment.id) +'/delete')

        checkComment = Comment.objects.filter(id=comment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkComment.count(), 1)

    def test_remove_comment_authenticated_and_is_comment_author(self):
        """
            Given a comment exists,
            When I try to remove the comment,
            Then I am redirected to the article page and the comment is removed
        """

        article = Article.objects.all().first()
        comment = Comment.objects.filter(article=article).first()
        
        self.client.login(username='commenttestuser', password='CommentTestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/comment/' + str(comment.id) +'/delete')

        checkComment = Comment.objects.filter(id=comment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkComment.count(), 0)

    def test_remove_comment_authenticated_and_is_article_author(self):
        """
            Given a comment exists,
            When I try to remove the comment as the article author,
            Then I am redirected to the article page and the comment is removed
        """

        article = Article.objects.all().first()
        comment = Comment.objects.filter(article=article).first()
        
        self.client.login(username='articleauthortestuser', password='ArticleAuthorTestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/comment/' + str(comment.id) +'/delete')

        checkComment = Comment.objects.filter(id=comment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkComment.count(), 0)

    def test_remove_comment_authenticated_and_is_admin(self):
        """
            Given a comment exists,
            When I try to remove the comment as an admin,
            Then I am redirected to the article page and the comment is removed
        """

        article = Article.objects.all().first()
        comment = Comment.objects.filter(article=article).first()
        
        self.client.login(username='admintestuser', password='AdminTestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/comment/' + str(comment.id) +'/delete')

        checkComment = Comment.objects.filter(id=comment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkComment.count(), 0)