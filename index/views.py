from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.models import User as DjangoUserModel
from django.contrib.auth import authenticate, login

from .forms import LoginForm
from utils.utils import error_message_from_form


class Index(View):

    def get(self, request):
        if not request.user.is_authenticated:
            loginForm = LoginForm()
            return render(request, "login.html", {'form': loginForm})
        else:
            return render(request, "home.html", {'user': request.user})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("/")

        form = LoginForm(request.POST)

        if not form.is_valid():
            content = error_message_from_form(form)
            return HttpResponse(content.strip(), content_type="text/plain", status=422)
        else:
            cleaned_data = form.cleaned_data
            credentials = {
                'username': cleaned_data['username'],
                'password': cleaned_data['password']
            }

            user = authenticate(request, **credentials)
            if user is None:
                return HttpResponse(
                "Authentication failed, please check your username or password",
                content_type="text/plain", status=403)

            login(request, user)

            return redirect("/")
