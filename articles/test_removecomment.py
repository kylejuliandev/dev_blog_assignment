from datetime import datetime
from django.test import TestCase
from accounts.models import User
from articles.models import Article, Comment
from articles.testhelpers import create_user, create_mock_article, create_mock_comment, get_random_string

class RemoveCommentTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        commentAuthor = create_user('CommentTestUser', 'CommentTestUser_P', False, False)
        create_user('OtherTestUser', 'OtherTestUser_P', False, False)
        create_user('AdminTestUser', 'AdminTestUser_P', False, True)
        articleAuthor = create_user('ArticleAuthorTestUser', 'ArticleAuthorTestUser_P', True, False)
        article = create_mock_article(articleAuthor)
        create_mock_comment(commentAuthor, article)

        return super().setUp()
    
    def tearDown(self) -> None:
        User.objects.all().delete()
        Article.objects.all().delete()
        return super().tearDown()
    
    def test_remove_comment_not_authenticated(self):
        article = Article.objects.all().first()
        comment = Comment.objects.filter(article=article).first()
        
        response = self.client.post('/article/' + str(article.id) + '/comment/' + str(comment.id) +'/delete')

        checkComment = Comment.objects.filter(id=comment.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(checkComment.count(), 1)

    def test_remove_comment_authenticated_but_not_author(self):
        article = Article.objects.all().first()
        comment = Comment.objects.filter(article=article).first()
        
        self.client.login(username='othertestuser', password='OtherTestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/comment/' + str(comment.id) +'/delete')

        checkComment = Comment.objects.filter(id=comment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkComment.count(), 1)

    def test_remove_comment_authenticated_and_is_comment_author(self):
        article = Article.objects.all().first()
        comment = Comment.objects.filter(article=article).first()
        
        self.client.login(username='commenttestuser', password='CommentTestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/comment/' + str(comment.id) +'/delete')

        checkComment = Comment.objects.filter(id=comment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkComment.count(), 0)

    def test_remove_comment_authenticated_and_is_article_author(self):
        article = Article.objects.all().first()
        comment = Comment.objects.filter(article=article).first()
        
        self.client.login(username='articleauthortestuser', password='ArticleAuthorTestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/comment/' + str(comment.id) +'/delete')

        checkComment = Comment.objects.filter(id=comment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkComment.count(), 0)

    def test_remove_comment_authenticated_and_is_admin(self):
        article = Article.objects.all().first()
        comment = Comment.objects.filter(article=article).first()
        
        self.client.login(username='admintestuser', password='AdminTestUser_P')
        response = self.client.post('/article/' + str(article.id) + '/comment/' + str(comment.id) +'/delete')

        checkComment = Comment.objects.filter(id=comment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(checkComment.count(), 0)