#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

__version__ = '1.0.0.0'

"""
@brief 简介 
@details 详细信息
@author  zhphuang
@data    2018-03-28 
"""


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码", "value": "", "required": "required"}),
                               min_length=5, max_length=20, error_messages={"required": "密码不能为空"})


class RegisterForm(forms.Form):
    username = forms.CharField(min_length = 3, max_length=20, error_messages={"required": "密码不能为空"})
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入绑定邮箱账号", "value": ""}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码", "value": "", "required": "required"}),
                               min_length=5, max_length=20, error_messages={"required": "密码不能为空"})