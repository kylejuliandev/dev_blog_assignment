from django.test import TestCase
from accounts.models import User
from articles.models import Article
from articles.testhelpers import create_mock_author, create_mock_articles

class HomeTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        """Sets up test data. Specifically, it creates a author user and 10 articles"""
        author = create_mock_author('TestUser', 'TestUser_P')
        create_mock_articles(author, 10)
        return super().setUp()
    
    def tearDown(self) -> None:
        """Tears down any test data, such as Users and Articles"""
        User.objects.all().delete()
        Article.objects.all().delete()
        return super().tearDown()
    
    def test_home_returns_paginated_articles(self):
        """
            Given articles exist,
            When I get articles,
            Then I am returned a paginated collection of articles
        """

        response = self.client.get('/')

        queryset = response.context['page_obj']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(queryset.number, 1)
        self.assertEqual(queryset.paginator.count, 10)
        self.assertEqual(queryset.paginator.num_pages, 4)
        self.assertEqual(queryset.paginator.per_page, 3)
    
    def test_home_returns_no_articles(self):
        """
            Given no articles exist,
            When I get articles,
            Then no articles are shown
        """

        Article.objects.all().delete()
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No articles have been written!', html=True)