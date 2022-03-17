from django.shortcuts import render
from django.views.generic import ListView
from articles.models import Article

class HomeListView(ListView):
    """Renders the home page, with a list of all articles."""
    model = Article

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

# Create your views here.
def home(request):
    return render(request, 'articles/home.html')