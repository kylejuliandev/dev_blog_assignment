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
    
    article = get_article(article_id)
    if request.method == 'POST':
        user = get_user(request)
        if user.is_authenticated:
            if article.author == user:
                article.delete()
                return redirect(reverse(viewname='home'))
    
    comments = get_comments(article_id)
    
    return render(request, 'articles/article.html', { 'article': article, 'comments': comments })

def comment(request, article_id:UUID):
    """Comment on an article"""
    
    if article_id == None:
        return redirect(reverse(viewname='home'))
    
    if not request.user.is_authenticated:
        return redirect(reverse(viewname='home'))

    existingArticle = get_article(article_id)

    if request.method == "POST":
        form = PublishCommentForm(request.POST)
        if form.is_valid():
            user = get_user(request)
            content = str(form.cleaned_data['content'])

            if len(content) > 280:
                form.add_error(field='content', error=ValidationError('Comment is too long'))
            
            if not form.errors:
                comment = Comment()
                comment.id = uuid4()
                comment.author = user
                comment.article = existingArticle
                comment.content = content
                comment.created_on = datetime.utcnow()
                comment.save()

                # Switch method to GET
                request.method = "GET"
                return article(request, article_id)
    else:
        form = PublishCommentForm()
    
    return render(request, 'articles/comment.html', { 'article': existingArticle, 'form': form, 'article_id': article_id })

def publish_article(request):
    """Presents the user with a form to create a article"""

    if request.user.is_authenticated:
        user = get_user(request)
        if user.is_author:
            if request.method == 'POST':
                form = PublishArticleForm(request.POST)

                if form.is_valid():
                    title = str(form.cleaned_data['title'])
                    summary = str(form.cleaned_data['summary'])
                    content = str(form.cleaned_data['content'])

                    if len(title) > 200:
                        form.add_error(field='title', error=ValidationError('Title is too long'))
                    
                    if len(summary) > 255:
                        form.add_error(field='title', error=ValidationError('Summary is too long'))
                    
                    if not form.errors:
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
                form = PublishArticleForm()

            return render(request, 'articles/publish.html', { 'form': form })
    else:
        return redirect(reverse(viewname='home'))

def edit_article(request, article_id):
    """Presents the user with a form to edit a article"""

    if request.user.is_authenticated:
        user = get_user(request)
        if user.is_author:
            existingArticle = get_article(article_id)
            if existingArticle != None and existingArticle.author == user:
                if request.method == 'POST':
                    form = PublishArticleForm(request.POST)

                    if form.is_valid():
                        title = str(form.cleaned_data['title'])
                        summary = str(form.cleaned_data['summary'])
                        content = str(form.cleaned_data['content'])

                        if len(title) > 200:
                            form.add_error(field='title', error=ValidationError('Title is too long'))
                        
                        if len(summary) > 255:
                            form.add_error(field='title', error=ValidationError('Summary is too long'))
                        
                        if not form.errors:
                            existingArticle.title = title
                            existingArticle.summary = summary
                            existingArticle.content = content
                            existingArticle.updated_on = datetime.utcnow()

                            existingArticle.save()

                            # We overwrite the request method to prevent instaneous deletion
                            request.method = "GET"
                            return article(request, existingArticle.id)
                else:
                    form = PublishArticleForm()
                    form.fields['title'].initial = existingArticle.title
                    form.fields['summary'].initial = existingArticle.summary
                    form.fields['content'].initial = existingArticle.content
                
                return render(request, 'articles/edit.html', { 'form': form })
    
    return redirect(reverse(viewname='home'))

def get_user(request) -> User:
    """Get authenticated user from the request"""

    return request.user

def get_article(article_id:UUID) -> Article:
    """Get article from the database with specified article_id"""

    return Article.objects.get(id=article_id)

def get_comments(article_id:UUID):

    return Comment.objects.filter(article=article_id)