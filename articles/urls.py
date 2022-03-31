from django.urls import path
from articles import views
from articles.models import Article

home_list_view = views.HomeListView.as_view(
    queryset=Article.objects.order_by('-created_on'),
    context_object_name='articles',
    template_name='articles/home.html'
)

urlpatterns = [
    path('', home_list_view, name='home'),
    path('article/<uuid:article_id>', views.article, name='article'),
    path('article/<uuid:article_id>/edit', views.edit_article, name='edit_article'),
    path('article/<uuid:article_id>/comment', views.comment, name='comment_article'),
    path('article', views.publish_article, name='publish_article'),
]