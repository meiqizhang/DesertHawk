from django.urls import path

from apps.linking import views

app_name = 'linking'

urlpatterns = [
    path("list/", views.list_links, name="list"),
    path("click/", views.click_links, name="click")
]