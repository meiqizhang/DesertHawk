from apps.gbook import views
from django.urls import path

app_name = 'gbook'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('add/', views.add, name='add'),
    path('ding/', views.ding, name='ding'),
    path('cai/', views.cai, name='cai'),
]