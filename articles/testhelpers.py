
from datetime import datetime
import random
import string
from uuid import UUID
from accounts.models import User
from articles.models import Article, Comment

def create_mock_author(username:str, password:str) -> User:
    """Create a new user with the specified details"""
    return create_user(username, password, True, False)

def create_mock_admin(username:str, password:str) -> User:
    """Create a new user with the specified details"""
    return create_user(username, password, False, True)

def create_user(username:str, password:str, isauthor:bool, isadmin:bool) -> User:
    user = User()
    user.username = username.lower()
    user.first_name = 'Test'
    user.last_name = 'User'
    user.is_author = isauthor
    user.is_active = True
    user.is_admin = isadmin
    user.set_password(password)
    user.save()

    return user

def create_mock_articles(author:User, count:int):
    for x in range(count):
        create_mock_article(author)

def create_mock_article(author:User) -> Article:
    article = Article()
    article.author = author
    article.title = get_random_string(200)
    article.summary = get_random_string(255)
    article.content = get_random_string(2000)
    article.created_on = datetime.utcnow()
    article.updated_on = datetime.utcnow()
    article.save()
    
    return article

def create_mock_comment(author:User, article:Article):
    comment = Comment()
    comment.author = author
    comment.article = article
    comment.content = 'Great article!'
    comment.created_on = datetime.utcnow()
    comment.save()

def get_random_string(length:int) -> str:
    return ''.join(random.choice(string.ascii_letters + string.punctuation + string.digits) for x in range(length))