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

from django.urls import path,include
from sqtp import views
from rest_framework.urlpatterns import format_suffix_patterns


# API文档生成器依赖的类
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions



schema_view=get_schema_view(  # schema_view的文档视图
    openapi.Info(
        title='SQTP APT DOC', # api页面的标题
        default_version='v1',
        description='SQTP接口文档',
        terms_of_service='王新科&宋文强',
        contact=openapi.Contact(email='wangxinke@sqtp.org'+'*'*10+'songwenqiang@sqtp.org',url='https:www.baidu.com'),
        license=openapi.License(name='BSD License') # 开源证书
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)



# 使用rf的框架自带的路由器生成路由列表
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# 将视图信息注册到路由列表即可
router.register(r'requests',views.RequestViewSet)
router.register(r'cases',views.CaseViewSet)
router.register(r'steps',views.StepViewSet)
router.register(r'projects',views.ProjectViewSet)
router.register(r'envs',views.EnvironmentViewSet)
router.register(r'plans',views.PlanViewSet)
router.register(r'reports',views.ReportViewSet)

# 解耦 就把代码给分离开来

# rest——fr的风格是主体url不变，requests/ 不变
urlpatterns = [
    # path('requests/',views.Requestlist.as_view()), # # 视图类需要as_view()转换
    # # path('requests/<int:_id>',views.ReauestDetail.as_view()) # 视图类需要as_view()转换
    # path('requests/<int:pk>',views.ReauestDetail.as_view()) # 视图类需要as_view()转换
    path('',include(router.urls)),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swageer-ui'), # name是对url的命名，类似别名，固定的  # # 互动模式
    path('redoc/',schema_view.with_ui('redoc',cache_timeout=0),name='schema-redoc'), # 文档模式,

    path('users/',views.user_list),
    path('users/<int:_id>',views.user_detail),
    # 注册
    path('register/',views.register),
    #登录
    path('login/',views.login),
    #登出
    path('logout/',views.logout),
    #当前用户信息
    path('current_user/',views.current_user),
    # 上传文件
    path('upload/<str:filename>/',views.FileUploadView.as_view()),

    path('customer/',views.customer_api) #测试文档效果接口，后期删除
            ]

# urlpatterns=format_suffix_patterns(urlpatterns)  # 返回 URL 模式列表，其中包括附加到所提供的每个 URL 格式后缀模式     这是其他的写法可以作为参考

