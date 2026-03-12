"""
 Copyright (C) 2026 Wojciech Szyba - All Rights Reserved
 You may use, distribute and modify this code under the
 terms of the GNU GENERAL PUBLIC LICENSE license,
 You should have received a copy of the license with
 this file. If not, please visit :
https://github.com/wojciech-szyba/wall-stash/blob/main/LICENSE
 */
"""

from .models import MemoriesModel
from .forms import LoginForm, RegisterForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib import messages
import re
from datetime import datetime

from .forms import MemoryForm


def mobile(request):
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


def index(request):
    template = loader.get_template('login.html')
    return HttpResponseRedirect(reverse('get_memories'))


@login_required
def get_memories(request, tag=None, type=None, date=None):
    memories = MemoriesModel.objects.filter(archived=0).order_by('-date')

    if mobile(request):
        template = loader.get_template('kafelki_mobile.html')
    else:
        template = loader.get_template('kafelki.html')
    tags = []
    types = []
    for memory in memories:
        tags = tags + memory.get_tags()
        types.append(memory.get_category)
        if type:
            if type not in memory.get_category:
                memories = memories.exclude(id=memory.id)
        if tag:
            if tag not in memory.get_tags():
                memories = memories.exclude(id=memory.id)
        if date:
            if datetime.strptime(date, "%Y-%m-%d").date() != memory.date.date():
                memories = memories.exclude(id=memory.id)
    tags = set(tags)
    types = set(types)
    context = {
        'memories': memories,
        'tags': tags,
        'types': types,
    }
    return HttpResponse(template.render(context, request))


@login_required
def delete_memo(request, id):
    memo = MemoriesModel.objects.get(id=id)
    memo.delete()
    return HttpResponseRedirect(reverse('get_memories'))


@login_required
def archive_memo(request, id):
    memo = MemoriesModel.objects.get(id=id)
    memo.archived = 1
    memo.save()
    return HttpResponseRedirect(reverse('get_memories'))


@login_required
def update_memo(request, id):
    memo = MemoriesModel.objects.get(id=id)
    if request.method == "POST":
        form = MemoryForm(request.POST)
        memo.content = form.content
        memo.save()
    return HttpResponseRedirect(reverse('get_memories'))


@login_required
def save_memo(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = MemoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        else:
            print(form.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MemoryForm()

    return render(request, "kafelki.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Nieprawidłowe dane logowania.')

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            return redirect('login_view')

    return render(request, 'register.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('login_view')
