from django.urls import path, re_path

from apps.articles.mindsay import views as mindsay

app_name = 'mindsay'

urlpatterns = [
    path('', mindsay.home, name='home'),
    re_path('^detail', mindsay.detail, name='detail'),
]