import json

import re
import simplejson
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.safestring import mark_safe

from index import forms

# util
from index.models import AcademicSubject, Direction, Department


# true = предметы
# fasle = напрпаления
def get_select_data(request):
    data = []
    if "type" in request.POST:
        type = request.POST["type"]
        if type == 'false':
            data = AcademicSubject.objects.all()
        elif type == 'true':
            data = Department.objects.all()
    json = simplejson.dumps([{'id': o.pk,
                              'text': o.name} for o in data])
    return HttpResponse(json)


# Util
def subset(a, b):
    if set(b.subjects_list.all()).issubset(set(a)):
        return b
    else:
        return None


# Util
def RepresentsInt(s):
    if len(s) <= 3:
        return True
    else:
        return False


# type = True предметы/False - направления
def search_data(request):
    directions_list = []
    type = None
    if 'search_form' in request.POST:
        if 'type' in request.POST:
            type = request.POST['type']
        ids = list(map(lambda x: x.split("=")[1], request.POST['search_form'].split("&")))
        if type == "false":
            subjects = AcademicSubject.objects.filter(id__in=ids)
            directions_list = [direct if subset(subjects, direct) else None for direct
                               in Direction.objects.all()]
        else:
            directions_list = Direction.objects.filter(department_fk__in=ids)
    directions_list = filter(lambda x: x is not None, directions_list)
    return render(request, 'result-search.html', {'directions': directions_list})


def login_user(request):
    data = request.POST.copy()
    if 'login' in data and 'password' in data:
        user = authenticate(username=str(data['login']), password=data['password'])
        if user is not None:
            login(request, user)
            if 'remember' in data:
                request.session.set_expiry(360 * 24 * 30)  # one month
            else:
                request.session.set_expiry(0)
    return redirect(index)


def logout_user(request):
    logout(request)
    return redirect(index)


def registration(request):
    data = request.POST.copy()
    if 'login' in data and 'password' in data and 'email' in data:
        user = User.objects.create_user(data['login'], data['email'], data['password'])
        user.save()
        login(request, user)
    return redirect(index)


def index(request):
    return render(request, "loggable-base.html", {"user": request.user})


def description(request):
    direction = None
    if 'id' in request.POST:
        direction = get_object_or_404(Direction, id=request.POST['id'])
    subjects = direction.subjects_list.all()
    print(direction.marks)
    values = [['Год', 'Балл']] + list(
        map(lambda x: list(map(lambda x: int(x) if RepresentsInt(x) else x, x.split(':'))),
            re.split(r" |, |,", direction.marks)))
    return render(request, "direction-info.html",
                  {"subjects": subjects, "direction": direction, "values": mark_safe(values)})
