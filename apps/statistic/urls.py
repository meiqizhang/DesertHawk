from django.urls import path

from apps.statistic import views

app_name = 'statistic'

urlpatterns = [
    path('get', views.get_statistic, name='get'),
]