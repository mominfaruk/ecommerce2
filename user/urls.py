from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/',sign_up, name='signup'),
    path('login', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout')
]