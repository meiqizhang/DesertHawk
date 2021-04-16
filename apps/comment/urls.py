from django.urls import path
from apps.comment import views

app_name = 'comment'

urlpatterns = [
    path('list', views.lists, name='list'),
    path('commit', views.commit, name='commit'),
    path('reply', views.reply, name='reply'),
    path('ding', views.ding, name='ding'),
    path('cai', views.cai, name='cai'),
    path('comment.html', views.comment_html, name='comment_html'),
]