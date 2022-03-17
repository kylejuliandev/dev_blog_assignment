from django.urls import path
from articles import views
from articles.models import Article

home_list_view = views.HomeListView.as_view(
    queryset=Article.objects.order_by('-created_on')[:5],
    context_object_name='articles',
    template_name='articles/home.html'
)

urlpatterns = [
    path('', home_list_view, name='home'),
]