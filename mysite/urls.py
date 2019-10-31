"""mysite URL Configuration

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
from django.urls import path, include
from login import views as login_views
from assets import views as assets_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 登陆模块url，后期整理出去到：login.urls.py

    path('login/', login_views.login),
    path('register/', login_views.register),
    path('logout/', login_views.logout),
    path('captcha/', include('captcha.urls')),
    path('confirm/', login_views.user_confirm),

    # 资产管理模块url，模块路径：assets.urls.py
    path('assets/', include('assets.urls')),
]
