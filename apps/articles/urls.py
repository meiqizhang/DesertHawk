from django.urls import path, include

from apps.articles import views

app_name = 'articles'

urlpatterns = [
    path('program/', include(('apps.articles.program.urls', 'program'), namespace='program')),
    path("d_icon/", views.download_icon)

    #path('detail/',         program.program_detail,   name='detail'),
    #path('write/',          views.write_article,    name='write'),
    #path('publish/',        views.upload_article,   name='publish'),
    #path('search/',         views.article_search,   name='search'),

    #path('program/',   program.program_home, name='program_home'),
    #path('article_image/',  views.article_image, name='article_image'),

    #path('upload_thumb/', views.upload_article_thumb),
    # path('manage/',         views.manage_article,   name='manage'),

    # 程序设计
    #path('program/', views.program_category, name='program'),

    # 旅行摄摄影
    #path('travel/', views.program_category, name='travel'),
]