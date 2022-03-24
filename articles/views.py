from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from articles.models import Article

class HomeListView(ListView):
    """Renders the home page, with a list of all articles."""
    model = Article
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

# Create your views here.
def home(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, per_page=3)
    page_number = request.GET('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'articles/home.html', { 'page_obj': page_obj })