from django.urls import path

from apps.articles.mindsay import views as mindsay

app_name = 'mindsay'

urlpatterns = [
    path('',   mindsay.home, name='home'),
   # path('detail',   travel.detail, name='detail'),
]