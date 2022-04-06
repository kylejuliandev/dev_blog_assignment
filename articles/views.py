from datetime import datetime
from uuid import UUID, uuid4
from django.forms import ValidationError
from accounts.models import User
from articles.admin import PublishArticleForm, PublishCommentForm
from articles.models import Article, Comment
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django.core.paginator import Paginator

import logging

logger = logging.getLogger(__name__)

class HomeListView(ListView):
    """Renders the home page, with a list of all articles."""
    model = Article
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def home(request):
    """Get paginated list of articles"""

    articles = Article.objects.all()
    paginator = Paginator(articles, per_page=3)
    page_number = request.GET('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'articles/home.html', { 'page_obj': page_obj })

def article(request, article_id:UUID):
    """Get specific article"""
    
    if article_id == None:
        return redirect(reverse(viewname='home'))
    
    user = get_user(request)

    try:
        logger.debug('Getting Article %s for User %s', article_id, user.username)
        article = get_article(article_id)
    except:
        logger.exception('Unable to get Article %s for User %s as the database retrieve failed', article_id, user.username)
        return redirect(reverse(viewname='home'))

    if request.method != 'POST':
        comments = get_comments(article_id)
        return render(request, 'articles/article.html', { 'article': article, 'comments': comments })
    
    if user is None or not user.is_authenticated:
        logger.warning('User tried to remove a article %s but they were not authenticated', article_id)
        comments = get_comments(article_id)
        return render(request, 'articles/article.html', { 'article': article, 'comments': comments })

    if article.author == user or user.is_admin:
        try:
            article.delete()
            logger.info('User %s removed article %s', str(user.username), str(article_id))
        except:
            logger.exception('Unable to delete Article %s for User %s as the database delete failed', article_id, user.username)

        return redirect(reverse(viewname='home'))
    else:
        logger.warning('Authenticated User %s tried to remove a article %s they had not published', user.username, article_id)
    
    comments = get_comments(article_id)
    return render(request, 'articles/article.html', { 'article': article, 'comments': comments })       

def comment(request, article_id:UUID):
    """Comment on an article"""
    
    if article_id == None:
        return redirect(reverse(viewname='home'))
    
    user = get_user(request)
    if not user.is_authenticated:
        logger.warning('Unauthenticated user tried to comment on an article')
        return redirect(reverse(viewname='home'))

    try:
        logger.debug('Getting Article %s for User %s', article_id, user.username)
        existingArticle = get_article(article_id)
    except:
        logger.debug('User %s requested Article %s that does not exist', user.username, article_id)
        return redirect(reverse(viewname='home'))

    if request.method != 'POST':
        form = PublishCommentForm()
        return render(request, 'articles/comment.html', { 'article': existingArticle, 'form': form, 'article_id': article_id })
    
    form = PublishCommentForm(request.POST)
    if form.is_valid():
        content = str(form.cleaned_data['content'])
        
        comment = Comment()
        comment.id = uuid4()
        comment.author = user
        comment.article = existingArticle
        comment.content = content
        comment.created_on = datetime.utcnow()

        try:
            comment.save()
            logger.info('Comment %s added to Article %s by User %s', comment.id, article_id, user.username)
        except:
            logger.exception('Unable to save Comment %s to the database for User %s on Article %s due to exception', comment.id, user.username, article_id)

        # Switch method to GET
        request.method = "GET"
        return article(request, article_id)
    else:
        logger.debug('User %s tried to publish a Comment on Article %s but it failed as the form was not valid', user.username, article_id)

    return render(request, 'articles/comment.html', { 'article': existingArticle, 'form': form, 'article_id': article_id })

def remove_comment(request, article_id:UUID, comment_id:UUID):
    user = get_user(request)
    if not user.is_authenticated:
        logger.warning('Unauthenticated User tried to remove Comment %s on Article %s', comment_id, article_id)
        return redirect(reverse(viewname='home'))
    
    try:
        comment = get_comment(article_id, comment_id)    
        if comment.author == user or user.is_admin or comment.article.author == user:
            comment.delete()
            logger.info('User %s removed Comment %s on Article %s', user.username, comment_id, article_id)
        else:
            logger.warning('User %s tried to remove a Comment %s they did not write', user.username, comment_id)

        request.method = "GET"
        return article(request, article_id)
    except:
        logger.exception('Unable to delete Comment %s on Article %s by User %s', comment_id, article_id, user.username)
        return article(request, article_id)

def publish_article(request):
    """Presents the user with a form to create a article"""

    user = get_user(request)

    if not user.is_authenticated:
        logger.warning('Unauthenticated User tried to publish an Article')
        return redirect(reverse(viewname='home'))
        
    if not user.is_author and not user.is_admin:
        logger.warning('User %s tried to publish an Article', user.username)
        return redirect(reverse(viewname='home'))

    if request.method != 'POST':
        form = PublishArticleForm()
        return render(request, 'articles/publish.html', { 'form': form })

    form = PublishArticleForm(request.POST)
    if form.is_valid():
        title = str(form.cleaned_data['title'])
        summary = str(form.cleaned_data['summary'])
        content = str(form.cleaned_data['content'])

        newArticle = Article()
        newArticle.id = uuid4()
        newArticle.author = user
        newArticle.title = title
        newArticle.summary = summary
        newArticle.content = content
        newArticle.created_on = datetime.utcnow()
        newArticle.updated_on = datetime.utcnow()

        newArticle.save()

        # We overwrite the request method to prevent instaneous deletion
        request.method = "GET"
        return article(request, newArticle.id)
    else:
        logger.debug('User %s tried to create Article but form validation failed', user.username)

    return render(request, 'articles/publish.html', { 'form': form })

def edit_article(request, article_id):
    """Presents the user with a form to edit a article"""

    user = get_user(request)
    if user == None or not request.user.is_authenticated:
        logger.warning('Unauthenticated user tried to edit Article')
        return redirect(reverse(viewname='home'))

    if not user.is_author and not user.is_admin:
        logger.warning('User %s tried to edit Article %s but they do not have permissions to do so', user.username, article_id)
        return redirect(reverse(viewname='home'))

    try:
        existingArticle = get_article(article_id)
    except:
        logger.warning('User %s tried to edit Article %s but it does not exist', user.username, article_id)
        return redirect(reverse(viewname='home'))

    if existingArticle == None:
        logger.warning('User %s tried to edit Article %s but it does not exist', user.username, article_id)
        return redirect(reverse(viewname='home'))

    if existingArticle.author != user and not user.is_admin:
        logger.warning('User %s tried to edit Article %s but they did not publish it', user.username, article_id)
        return redirect(reverse(viewname='home'))
    
    if request.method != 'POST':
        form = PublishArticleForm()
        form.fields['title'].initial = existingArticle.title
        form.fields['summary'].initial = existingArticle.summary
        form.fields['content'].initial = existingArticle.content
        return render(request, 'articles/edit.html', { 'form': form })
   
    form = PublishArticleForm(request.POST)

    if form.is_valid():
        title = str(form.cleaned_data['title'])
        summary = str(form.cleaned_data['summary'])
        content = str(form.cleaned_data['content'])

        existingArticle.title = title
        existingArticle.summary = summary
        existingArticle.content = content
        existingArticle.updated_on = datetime.utcnow()

        existingArticle.save()
        logger.info('User %s edited Article %s', user.username, article_id)

        # We overwrite the request method to prevent instaneous deletion
        request.method = "GET"
        return article(request, existingArticle.id)
    else:
        logger.debug('User %s tried to edit Article %s but they submitted a form with errors', user.username, article_id)

    return render(request, 'articles/edit.html', { 'form': form })

def get_user(request) -> User:
    """Get authenticated user from the request"""

    return request.user

def get_article(article_id:UUID) -> Article:
    """Get article from the database with specified article_id"""

    return Article.objects.get(id=article_id)

def get_comments(article_id:UUID):
    """Get comments related to an article"""
    return Comment.objects.filter(article=article_id)

def get_comment(article_id:UUID, comment_id:UUID):
    """Get comment related to a specific article"""
    return Comment.objects.get(article=article_id, id=comment_id)