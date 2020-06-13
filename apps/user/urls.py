from apps.user import views
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('regist/', views.regist, name='regist'),
    path('send_code/', views.send_code, name='send_code'),
]

'''
path('register/', views.user_register, name = 'register'),
#path('login/', views.user_login, name = 'user_login'), user_statstic
path('statistic/set', views.user_statistic, name = 'set_statistic'),
path('statistic/get', views.get_statistic, name = 'get_statistic'),
path('login/', views.login_qq, name = 'user_login'),
#path('login/', include('social_django.urls', namespace='social'), name = 'user_login'),
path('logout/', views.user_logout, name = 'user_logout'),
path('sendcode/', views.send_code, name = 'send_code'),
path('codelogin/', views.code_login, name = 'code_login'),
path('forgetpassword/', views.forget_password, name = 'forget_password'),
path('updatepwd/', views.update_pwd, name = 'update_pwd'),
path('valide_code/', views.valide_code, name = 'valide_code'),
# path('center/', views.user_center, name = 'center'),   #本地存储
path('center/', views.user_center, name = 'center'), #云存储
path('gbook/', views.gbook, name = 'gbook'), #云存储
'''