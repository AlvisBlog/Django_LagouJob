import json
from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import UserProfile
from .forms import LoginForm, RegisterForm
from django.contrib.auth.hashers import make_password
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "users/login.html", {"msg":"用户名或密码错误！"})
        else:
            return render(request, "users/login.html", {"login_form": login_form})


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("users:login"))


class RegisterView(View):

    def get(self, request):
        return render(request, "users/register.html")

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("username", "")
            email = request.POST.get("email", "")
            if UserProfile.objects.filter(Q(username=user_name) | Q(email=email)):
                return HttpResponse(json.dumps({"status": -1, "msg": "用户已经存在"}), content_type = 'application/json')
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = email
            user_profile.is_active = True
            user_profile.password = make_password(pass_word)
            user_profile.save()
            return render(request, "users/register.html", {"msg":"注册成功！<a href='/users/login' class='am-btn am-btn-default'>去登陆</a>"})
        else:
            msg = ""
            for key, error in register_form.errors.items():
                msg += "<p>%s</p>" % error
            return render(request, "users/register.html", {"msg": msg})