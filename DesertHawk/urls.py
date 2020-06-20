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

    # #path('xadmin/', xadmin.site.urls),
    # path('calendar/', common.calendar),
    # path('about/', common.about_me),
    # path('upload_image/', common.content_image_manager),
    # path('download_image/', common.content_image_manager),
    # path('starttime/', common.get_start_time),
    # #path('', include('social_django.urls', namespace='social'), name='user_login'),
    path('', include(('apps.home.urls'), namespace="index")),
    path('home/', include(('apps.home.urls'), namespace="home")),
    # #path('user/', include(('User.urls', 'user'), namespace='user')),
    path('articles/', include(('apps.articles.urls', 'articles'), namespace='articles')),
    # #re_path(r'^captcha/', include('captcha.urls')),
    # re_path(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),
    # #re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]