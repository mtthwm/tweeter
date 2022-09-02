"""tweeter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from homepage.views import UserView, IndexView, LikePostView, SearchHistoryView
from accounts.views import SignInView, SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('user/<str:username>/', UserView.as_view()),
    path('like_post/<int:post_id>', LikePostView.as_view()),
    path('accounts/sign_in', SignInView.as_view()),
    path('accounts/sign_up', SignUpView.as_view()),
    path('search_history/<int:search_id>', SearchHistoryView.as_view()),
]
