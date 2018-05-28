import json
import copy
from django.shortcuts import render
from django.views.generic.base import View
from django.db import connection
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils.custom_paginator import CustomPaginator
from django.core.paginator import EmptyPage, PageNotAnInteger
from .models import DataModel
from django.contrib.auth.decorators import login_required
from django.db.models import Q


class LoginRequiredMixin(object):
    """
    登陆限定，并指定登陆url
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='/users/login')

# Create your views here.
class IndexView(LoginRequiredMixin, View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

    def get(self, request):

        # if skill_type and int(skill_type) in range(0, 7):
        #    data_records = DataModel.objects.filter(skill_type=int(skill_type))
        #else:
        data_records = DataModel.objects.all()
        current_page = request.GET.get("page", '1')
        paginator = CustomPaginator(current_page, 9, data_records, 10)
        try:
            paginator = paginator.page(current_page)  #获取前端传过来显示当前页的数据
        except PageNotAnInteger:
            # 如果有异常则显示第一页
            paginator = paginator.page(1)
        except EmptyPage:
            # 如果没有得到具体的分页内容的话,则显示最后一页
            paginator = paginator.page(paginator.num_pages)
        return render(request, 'index.html', {"data_records": data_records, "paginator":paginator})

    def post(self, request):
        _type = request.POST.get("type")
        with connection.cursor() as cursor:
            if int(_type) == 1:
                skill_map = {0: "后端开发", 1: "移动开发", 2: "前端开发", 3: "前端开发", 4: "测试", 5: "运维", 6: "数据库"}
                sql = "SELECT count(*), skill_type from myapp_datamodel group by skill_type order by skill_type"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                for item in ret:
                    data.append({"value": item[0], "name": skill_map[item[1]]})
                return HttpResponse(json.dumps({"data": data}), content_type = 'application/json')

            if int(_type) == 2:
                sql = "SELECT count(*), left(position,2) from myapp_datamodel group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    data.append({"value": item[0], "name": item[1]})
                return HttpResponse(json.dumps({"data": data, "locations": locations}), content_type = 'application/json')

            if int(_type) == 3:
                sql = "SELECT avg(money), left(position,2) from myapp_datamodel group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                money = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    money.append(item[0])
                return HttpResponse(json.dumps({"money": money, "locations": locations}), content_type = 'application/json')

            if int(_type) == 4:
                sql = "SELECT count(*), rongzi from myapp_datamodel group by rongzi"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                rongzi = []
                for item in ret:
                    rongzi.append(item[1])
                    data.append({"value": item[0], "name": item[1]})
                return HttpResponse(json.dumps({"data": data, "rongzi": rongzi}), content_type = 'application/json')


class IndexView1(LoginRequiredMixin, View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(IndexView1, self).dispatch(*args, **kwargs)

    def get(self, request):

        # if skill_type and int(skill_type) in range(0, 7):
        #    data_records = DataModel.objects.filter(skill_type=int(skill_type))
        #else:
        data_records = DataModel.objects.filter(skill_type = 0)
        current_page = request.GET.get("page", '1')
        paginator = CustomPaginator(current_page, 9, data_records, 10)
        try:
            paginator = paginator.page(current_page)  #获取前端传过来显示当前页的数据
        except PageNotAnInteger:
            # 如果有异常则显示第一页
            paginator = paginator.page(1)
        except EmptyPage:
            # 如果没有得到具体的分页内容的话,则显示最后一页
            paginator = paginator.page(paginator.num_pages)
        return render(request, 'index1.html', {"data_records": data_records, "paginator":paginator})

    def post(self, request):
        _type = request.POST.get("type")
        with connection.cursor() as cursor:
            if int(_type) == 1:
                sql = "SELECT avg(money), left(position,2) from myapp_datamodel where skill_type=0 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                money = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    money.append(item[0])
                return HttpResponse(json.dumps({"money": money, "locations": locations}), content_type = 'application/json')

            if int(_type) == 2:
                sql = "SELECT count(*), left(position,2) from myapp_datamodel where skill_type=0 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "locations": locations}), content_type = 'application/json')

            if int(_type) == 3:
                sql = "SELECT count(*), exp from myapp_datamodel where skill_type=0 group by exp"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                exp = []
                for item in ret:
                    exp.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "exp": exp}), content_type = 'application/json')

            if int(_type) == 4:
                sql = "SELECT count(*), xueli from myapp_datamodel where skill_type=0 group by xueli"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                xueli = []
                for item in ret:
                    xueli.append(item[1])
                    data.append({"value": item[0], "name": item[1]})
                return HttpResponse(json.dumps({"data": data, "xueli": xueli}), content_type = 'application/json')


class IndexView2(LoginRequiredMixin, View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(IndexView2, self).dispatch(*args, **kwargs)

    def get(self, request):

        # if skill_type and int(skill_type) in range(0, 7):
        #    data_records = DataModel.objects.filter(skill_type=int(skill_type))
        #else:
        data_records = DataModel.objects.filter(skill_type = 1)
        current_page = request.GET.get("page", '1')
        paginator = CustomPaginator(current_page, 9, data_records, 10)
        try:
            paginator = paginator.page(current_page)  #获取前端传过来显示当前页的数据
        except PageNotAnInteger:
            # 如果有异常则显示第一页
            paginator = paginator.page(1)
        except EmptyPage:
            # 如果没有得到具体的分页内容的话,则显示最后一页
            paginator = paginator.page(paginator.num_pages)
        return render(request, 'index2.html', {"data_records": data_records, "paginator":paginator})

    def post(self, request):
        _type = request.POST.get("type")
        with connection.cursor() as cursor:
            if int(_type) == 1:
                sql = "SELECT avg(money), left(position,2) from myapp_datamodel where skill_type=1 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                money = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    money.append(item[0])
                return HttpResponse(json.dumps({"money": money, "locations": locations}), content_type = 'application/json')

            if int(_type) == 2:
                sql = "SELECT count(*), left(position,2) from myapp_datamodel where skill_type=1 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "locations": locations}), content_type = 'application/json')

            if int(_type) == 3:
                sql = "SELECT count(*), exp from myapp_datamodel where skill_type=1 group by exp"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                exp = []
                for item in ret:
                    exp.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "exp": exp}), content_type = 'application/json')

            if int(_type) == 4:
                sql = "SELECT count(*), xueli from myapp_datamodel where skill_type=1 group by xueli"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                xueli = []
                for item in ret:
                    xueli.append(item[1])
                    data.append({"value": item[0], "name": item[1]})
                return HttpResponse(json.dumps({"data": data, "xueli": xueli}), content_type = 'application/json')


class IndexView3(LoginRequiredMixin, View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(IndexView3, self).dispatch(*args, **kwargs)

    def get(self, request):

        # if skill_type and int(skill_type) in range(0, 7):
        #    data_records = DataModel.objects.filter(skill_type=int(skill_type))
        #else:
        data_records = DataModel.objects.filter(skill_type = 2)
        current_page = request.GET.get("page", '1')
        paginator = CustomPaginator(current_page, 9, data_records, 10)
        try:
            paginator = paginator.page(current_page)  #获取前端传过来显示当前页的数据
        except PageNotAnInteger:
            # 如果有异常则显示第一页
            paginator = paginator.page(1)
        except EmptyPage:
            # 如果没有得到具体的分页内容的话,则显示最后一页
            paginator = paginator.page(paginator.num_pages)
        return render(request, 'index3.html', {"data_records": data_records, "paginator":paginator})

    def post(self, request):
        _type = request.POST.get("type")
        with connection.cursor() as cursor:
            if int(_type) == 1:
                sql = "SELECT avg(money), left(position,2) from myapp_datamodel where skill_type=2 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                money = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    money.append(item[0])
                return HttpResponse(json.dumps({"money": money, "locations": locations}), content_type = 'application/json')

            if int(_type) == 2:
                sql = "SELECT count(*), left(position,2) from myapp_datamodel where skill_type=2 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "locations": locations}), content_type = 'application/json')

            if int(_type) == 3:
                sql = "SELECT count(*), exp from myapp_datamodel where skill_type=2 group by exp"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                exp = []
                for item in ret:
                    exp.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "exp": exp}), content_type = 'application/json')

            if int(_type) == 4:
                sql = "SELECT count(*), xueli from myapp_datamodel where skill_type=2 group by xueli"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                xueli = []
                for item in ret:
                    xueli.append(item[1])
                    data.append({"value": item[0], "name": item[1]})
                return HttpResponse(json.dumps({"data": data, "xueli": xueli}), content_type = 'application/json')


class IndexView4(LoginRequiredMixin, View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(IndexView4, self).dispatch(*args, **kwargs)

    def get(self, request):

        # if skill_type and int(skill_type) in range(0, 7):
        #    data_records = DataModel.objects.filter(skill_type=int(skill_type))
        #else:
        data_records = DataModel.objects.filter(skill_type = 3)
        current_page = request.GET.get("page", '1')
        paginator = CustomPaginator(current_page, 9, data_records, 10)
        try:
            paginator = paginator.page(current_page)  #获取前端传过来显示当前页的数据
        except PageNotAnInteger:
            # 如果有异常则显示第一页
            paginator = paginator.page(1)
        except EmptyPage:
            # 如果没有得到具体的分页内容的话,则显示最后一页
            paginator = paginator.page(paginator.num_pages)
        return render(request, 'index4.html', {"data_records": data_records, "paginator":paginator})

    def post(self, request):
        _type = request.POST.get("type")
        with connection.cursor() as cursor:
            if int(_type) == 1:
                sql = "SELECT avg(money), left(position,2) from myapp_datamodel where skill_type=3 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                money = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    money.append(item[0])
                return HttpResponse(json.dumps({"money": money, "locations": locations}), content_type = 'application/json')

            if int(_type) == 2:
                sql = "SELECT count(*), left(position,2) from myapp_datamodel where skill_type=3 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "locations": locations}), content_type = 'application/json')

            if int(_type) == 3:
                sql = "SELECT count(*), exp from myapp_datamodel where skill_type=3 group by exp"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                exp = []
                for item in ret:
                    exp.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "exp": exp}), content_type = 'application/json')

            if int(_type) == 4:
                sql = "SELECT count(*), xueli from myapp_datamodel where skill_type=3 group by xueli"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                xueli = []
                for item in ret:
                    xueli.append(item[1])
                    data.append({"value": item[0], "name": item[1]})
                return HttpResponse(json.dumps({"data": data, "xueli": xueli}), content_type = 'application/json')


class IndexView5(LoginRequiredMixin, View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(IndexView5, self).dispatch(*args, **kwargs)

    def get(self, request):

        # if skill_type and int(skill_type) in range(0, 7):
        #    data_records = DataModel.objects.filter(skill_type=int(skill_type))
        #else:
        data_records = DataModel.objects.filter(skill_type = 4)
        current_page = request.GET.get("page", '1')
        paginator = CustomPaginator(current_page, 9, data_records, 10)
        try:
            paginator = paginator.page(current_page)  #获取前端传过来显示当前页的数据
        except PageNotAnInteger:
            # 如果有异常则显示第一页
            paginator = paginator.page(1)
        except EmptyPage:
            # 如果没有得到具体的分页内容的话,则显示最后一页
            paginator = paginator.page(paginator.num_pages)
        return render(request, 'index5.html', {"data_records": data_records, "paginator":paginator})

    def post(self, request):
        _type = request.POST.get("type")
        with connection.cursor() as cursor:
            if int(_type) == 1:
                sql = "SELECT avg(money), left(position,2) from myapp_datamodel where skill_type=4 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                money = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    money.append(item[0])
                return HttpResponse(json.dumps({"money": money, "locations": locations}), content_type = 'application/json')

            if int(_type) == 2:
                sql = "SELECT count(*), left(position,2) from myapp_datamodel where skill_type=4 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "locations": locations}), content_type = 'application/json')

            if int(_type) == 3:
                sql = "SELECT count(*), exp from myapp_datamodel where skill_type=4 group by exp"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                exp = []
                for item in ret:
                    exp.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "exp": exp}), content_type = 'application/json')

            if int(_type) == 4:
                sql = "SELECT count(*), xueli from myapp_datamodel where skill_type=4 group by xueli"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                xueli = []
                for item in ret:
                    xueli.append(item[1])
                    data.append({"value": item[0], "name": item[1]})
                return HttpResponse(json.dumps({"data": data, "xueli": xueli}), content_type = 'application/json')


class IndexView6(LoginRequiredMixin, View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(IndexView6, self).dispatch(*args, **kwargs)

    def get(self, request):

        # if skill_type and int(skill_type) in range(0, 7):
        #    data_records = DataModel.objects.filter(skill_type=int(skill_type))
        #else:
        data_records = DataModel.objects.filter(skill_type = 5)
        current_page = request.GET.get("page", '1')
        paginator = CustomPaginator(current_page, 9, data_records, 10)
        try:
            paginator = paginator.page(current_page)  #获取前端传过来显示当前页的数据
        except PageNotAnInteger:
            # 如果有异常则显示第一页
            paginator = paginator.page(1)
        except EmptyPage:
            # 如果没有得到具体的分页内容的话,则显示最后一页
            paginator = paginator.page(paginator.num_pages)
        return render(request, 'index6.html', {"data_records": data_records, "paginator":paginator})

    def post(self, request):
        _type = request.POST.get("type")
        with connection.cursor() as cursor:
            if int(_type) == 1:
                sql = "SELECT avg(money), left(position,2) from myapp_datamodel where skill_type=5 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                money = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    money.append(item[0])
                return HttpResponse(json.dumps({"money": money, "locations": locations}), content_type = 'application/json')

            if int(_type) == 2:
                sql = "SELECT count(*), left(position,2) from myapp_datamodel where skill_type=5 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "locations": locations}), content_type = 'application/json')

            if int(_type) == 3:
                sql = "SELECT count(*), exp from myapp_datamodel where skill_type=5 group by exp"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                exp = []
                for item in ret:
                    exp.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "exp": exp}), content_type = 'application/json')

            if int(_type) == 4:
                sql = "SELECT count(*), xueli from myapp_datamodel where skill_type=5 group by xueli"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                xueli = []
                for item in ret:
                    xueli.append(item[1])
                    data.append({"value": item[0], "name": item[1]})
                return HttpResponse(json.dumps({"data": data, "xueli": xueli}), content_type = 'application/json')


class IndexView7(LoginRequiredMixin, View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(IndexView7, self).dispatch(*args, **kwargs)

    def get(self, request):

        # if skill_type and int(skill_type) in range(0, 7):
        #    data_records = DataModel.objects.filter(skill_type=int(skill_type))
        #else:
        data_records = DataModel.objects.filter(skill_type = 6)
        current_page = request.GET.get("page", '1')
        paginator = CustomPaginator(current_page, 9, data_records, 10)
        try:
            paginator = paginator.page(current_page)  #获取前端传过来显示当前页的数据
        except PageNotAnInteger:
            # 如果有异常则显示第一页
            paginator = paginator.page(1)
        except EmptyPage:
            # 如果没有得到具体的分页内容的话,则显示最后一页
            paginator = paginator.page(paginator.num_pages)
        return render(request, 'index7.html', {"data_records": data_records, "paginator":paginator})

    def post(self, request):
        _type = request.POST.get("type")
        with connection.cursor() as cursor:
            if int(_type) == 1:
                sql = "SELECT avg(money), left(position,2) from myapp_datamodel where skill_type=6 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                money = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    money.append(item[0])
                return HttpResponse(json.dumps({"money": money, "locations": locations}), content_type = 'application/json')

            if int(_type) == 2:
                sql = "SELECT count(*), left(position,2) from myapp_datamodel where skill_type=6 " \
                      "group by left(position,2) limit 20"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                locations = []
                for item in ret:
                    locations.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "locations": locations}), content_type = 'application/json')

            if int(_type) == 3:
                sql = "SELECT count(*), exp from myapp_datamodel where skill_type=6 group by exp"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                exp = []
                for item in ret:
                    exp.append(item[1])
                    data.append(item[0])
                return HttpResponse(json.dumps({"data": data, "exp": exp}), content_type = 'application/json')

            if int(_type) == 4:
                sql = "SELECT count(*), xueli from myapp_datamodel where skill_type=6 group by xueli"
                cursor.execute(sql)
                ret = cursor.fetchall()
                data = []
                xueli = []
                for item in ret:
                    xueli.append(item[1])
                    data.append({"value": item[0], "name": item[1]})
                return HttpResponse(json.dumps({"data": data, "xueli": xueli}), content_type = 'application/json')
