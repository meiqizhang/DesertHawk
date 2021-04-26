from django.urls import path

from apps.live import views

app_name = 'live'

urlpatterns = [
    path("", views.live, name="live")
]