from apps.search import views
from django.urls import path

app_name = 'search'

urlpatterns = [
    path('', views.search, name='search'),
]