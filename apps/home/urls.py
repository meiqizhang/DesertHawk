from django.urls import path, re_path

from apps.articles import views as article_views
from apps.home import views

app_name = 'index'

urlpatterns = [
    path('', views.home, name='home'),
]