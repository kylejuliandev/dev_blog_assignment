from django.urls import path
from accounts import views

urlpatterns = [
    path('login', views.signin, name='login'),
    path('logoff', views.signout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('manage', views.manage, name='manage'),
    path('closeaccount', views.closeaccount, name='closeaccount'),
]