from articles.models import Article
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

def article(request, article_id):
    """Get specific article"""
    
    if article_id == None:
        return redirect(reverse(viewname='home'))

    article = Article.objects.get(id=article_id)
    
    return render(request, 'articles/article.html', { 'article': article })