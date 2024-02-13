"""
URL configuration for QnA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from questions.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name='home_screen'),
    path('login/', auth_views.LoginView.as_view(template_name='questions/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='questions/logout.html'), name='logout'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('questions/', question_list, name='question_list'),
    path('ask/', ask_question, name='ask_question'),
    path('questions/<int:pk>/', question_detail, name='question_detail'),
    path('answer_question/<int:question_id>/', answer_question, name='answer_question'),
    path('questions/<int:question_id>/answer/<int:answer_id>/upvote/', upvote_answer, name='upvote_answer'),
    path('questions/<int:question_id>/answer/<int:answer_id>/downvote/', downvote_answer, name='downvote_answer'),
      path('increment_counter/', increment_counter, name='increment_counter'),
]
