from apps.document import views
from django.urls import path

app_name = 'document'

urlpatterns = [
    path('', views.list, name='list'),
]