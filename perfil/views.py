from django.shortcuts import render
from django.views.generic import View

from django.contrib.auth.models import User
from django.contrib import auth

from . import forms, models


# Create your views here.
class BaseUserProfile(View):
    template_name = 'perfil/register.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        user = self.request.user if not self.request.user.is_anonymous else None

        self.context = {
            'userform': forms.UserForm(
                user=user if user else None,
                data=self.request.POST or None,
                instance=user if user else None,
            ),
            'profileform': forms.UserProfileForm(data=self.request.POST or None),
        }

        self.render_template = render(
            self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):

        return self.render_template

    def get(self, *args, **kwargs):

        return self.render_template


class Register(BaseUserProfile):
    pass


class Update(BaseUserProfile):
    pass


class Login(View):
    pass


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    
    return render(request)
