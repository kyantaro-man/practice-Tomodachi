"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from friendslist import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('login/', views.Login.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', views.signup),
    path('create/', views.create),
    path('category/create/', views.category_create),
    path('category/<slug:pk>/', views.category_index),
    path('category/<slug:pk>/delete/', views.category_delete, name="category_delete"),
    path('<slug:pk>/', views.friend, name="friend"),
    path('<slug:pk>/delete', views.delete, name="delete"),
    path('<slug:pk>/memo/create/', views.memo_create, name="memo_create"),
    path('<slug:pk>/memo/<slug:memo_pk>/delete/', views.memo_delete, name="memo_delete"),
]
