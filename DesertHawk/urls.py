"""DesertHawk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from DesertHawk import view
from DesertHawk.view import get_start_time

urlpatterns = [
    path(r'mdeditor/', include('libs.mdeditor.urls')),
    path('admin/', admin.site.urls),
    path('starttime/', get_start_time),
    path('statistic/', include(('apps.statistic.urls', 'statistic'), namespace='statistic')),
    path('comment/', include(('apps.comment.urls'), namespace='comment')),
    path('user/', include(('apps.user.urls'), namespace='user')),
    path('gbook/', include(('apps.gbook.urls'), namespace='gbook')),
    path('aboutme/', include(('apps.aboutme.urls'), namespace='aboutme')),
    path('search/', include(('apps.search.urls'), namespace='search')),
    path('document/', include(('apps.document.urls'), namespace='document')),
    path('', include(('apps.home.urls'), namespace="index")),
    path('home/', include(('apps.home.urls'), namespace="home")),
    path('articles/', include(('apps.articles.urls', 'articles'), namespace='articles')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('robots.txt', view.robots),
    path('calendar.html', view.calendar)
]