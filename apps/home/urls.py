from django.urls import path

from apps.home import views

app_name = 'index'

urlpatterns = [
    path('', views.home, name='home'),
    path("fetch_news/", views.fetch_news, name="fetch_news")
    #path('home', views.home, name='home'),
    #path('index.html', views.home, name=''),
]