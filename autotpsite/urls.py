"""autotpsite URL Configuration

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
from django.urls import path,include
from sqtp import views
from sqtp import urls as sqtp_urls

# 静态文件服务
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # 不动
    path('api/',include(sqtp_urls))  # api开头的url都交给sqtp_urls中的视图函数处理,
    # 路由分发，url的前缀
    # path('sgin/',include('sgin_urls'))
    # path('sqtp/',include('sqtp_urls'))
            ]+static("/",document_root='dist') #如果不是就去访问静态资源文件

