from django.urls import path
from accounts import views

urlpatterns = [
    path('login', views.signin, name='login'),
    path('logoff', views.signout, name='logout')
]