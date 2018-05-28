"""lagou_new_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from myapp.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name = 'index'),
    url('^users/', include('users.urls', namespace = "users")),
    url(r'^index1/$', IndexView1.as_view(), name = 'index1'),
    url(r'^index2/$', IndexView2.as_view(), name = 'index2'),
    url(r'^index3$', IndexView3.as_view(), name = 'index3'),
    url(r'^index4$', IndexView4.as_view(), name = 'index4'),
    url(r'^index5$', IndexView5.as_view(), name = 'index5'),
    url(r'^index6$', IndexView6.as_view(), name = 'index6'),
    url(r'^index7$', IndexView7.as_view(), name = 'index7'),
]
