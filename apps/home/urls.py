from django.urls import path


from apps.home import views

app_name = 'index'

urlpatterns = [
    path('', views.home, name='home'),
]