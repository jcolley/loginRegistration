# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User


# Create your views here.
def index(request):
    return render(request, 'login_registration/index.html')


def register(request):
    results = User.objects.registerVal(request.POST)
    if not results['status']:
        for error in results['errors']:
            messages.error(request, error)
    else:
        messages.success(request, 'User created, please login.')

    return redirect('auth:index')


def login(request):
    results = User.objects.loginVal(request.POST)
    if not results['status']:
        for error in results['errors']:
            messages.error(request, error)
    else:
        request.session['id'] = results['user'].id
        return redirect('auth:success')
    return redirect('/')


def logout(request):
    request.session.clear()
    return rediect('auth:index')


def success(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        'user': user,
    }
    return render(request, 'login_registration/success.html', context)
