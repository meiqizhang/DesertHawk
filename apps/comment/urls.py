from django.urls import path
from apps.comment.views import commit, lists

app_name = 'comment'

urlpatterns = [
    path('list', lists, name='list'),
    path('commit', commit, name='commit'),
]