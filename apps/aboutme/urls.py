from django.urls import path

from apps.aboutme import views

app_name = 'aboutme'

urlpatterns = [
    path('', views.about, name='about'),
]