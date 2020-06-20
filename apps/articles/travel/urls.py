from django.urls import path

from apps.articles.travel import views as travel

app_name = 'travel'

urlpatterns = [

    path('',   travel.home, name='home'),
   # path('detail',   travel.detail, name='detail'),
]