from django.conf.urls import url
from django.urls import path

from apps.photos import views

app_name = 'photos'

urlpatterns = [
    path('', views.album, name='album'),
    url(r"^album/detail/", views.detail, name='detail'),
]