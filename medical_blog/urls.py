"""
URL configuration for medical_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('create/', views.create_article, name='create_article'),
    path('about/', views.about_view),
    path('list/', views.article_list, name='article_list'),

    path('<int:article_id>/comment/', views.article_comment),
    path('<int:article_id>/update/', views.update_article, name='update_article'),
    path('<int:article_id>/delete/', views.delete_article, name='delete_article'),

    path('topics/', views.topics_list_view, name='topics_list'),
    path('topics/<str:topic_title>/', views.topics_view, name='topic'),
    path('topics/<str:topic_title>/subscribe/', views.topic_subscribe, name='topic_subscribe'),
    path('topics/<str:topic_title>/unsubscribe/', views.topic_unsubscribe, name='topic_unsubscribe'),

    path('users/', views.user_profiles_list, name='user_profiles_list'),
    path('preferred_articles/<int:user_id>/', views.preferred_articles, name='preferred_articles'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('set-password/', views.set_password),
    path('set-userdata/', views.set_userdata),
    path('deactivate/', views.deactivate_profile),
    path('register/', views.register_profile, name='register'),
    path('login/', views.login_profile, name='login'),
    path('logout/', views.logout_profile),

    re_path(r'archive\/\d{4}\/[01]?\d{1}\/', views.regex),

    path('<int:article_id>/', views.article_detail_view, name='article_detail_view'),
]
