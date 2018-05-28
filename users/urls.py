#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0.0.0'
from django.conf.urls import url
from .views import LoginView, RegisterView,LogoutView


"""
@brief 简介 
@details 详细信息
@author  zhphuang
@data    2018-03-28 
"""

urlpatterns = [
    url(r'login/', LoginView.as_view(), name="login"),
    url(r'logout/', LogoutView.as_view(), name="logout"),
    url('register/', RegisterView.as_view(), name="register"),
]