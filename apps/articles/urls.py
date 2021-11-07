from django.urls import path, re_path

from apps.articles import views

app_name = 'articles'

urlpatterns = [
    path("d_icon/", views.download_icon),
    path("u_icon/", views.upload_icon),
    path("update_cover_pic", views.update_cover_pic),
    path("programing", views.programing),
    re_path("^p/", views.detail),
]