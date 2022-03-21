from django.shortcuts import render
from django.views.generic import View

from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.
class Register(View):
    pass


class Login(View):
    pass


class Update(View):
    pass


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    
    return render(request)
