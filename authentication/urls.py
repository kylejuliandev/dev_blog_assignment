from django.urls import path
from authentication import views

urlpatterns = [
    path('login', views.signin, name='login'),
    path('logoff', views.signout, name='logout')
]