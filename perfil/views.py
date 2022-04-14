from django.shortcuts import redirect, render
from django.urls import reverse

from django.views.generic import View

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User

import copy

from . import forms


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
            'loginform': forms.LoginForm(
                request=self.request,
                data=self.request.POST or None),
        }

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        self.render_template = render(
            self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            datas = self.request.POST

            login_username = datas.get('login_username')
            login_password = datas.get('login_password')

            if not login_username and not login_password:
                email = datas.get('email')
                username = datas.get('username')
                password = datas.get('password')
                first_name = datas.get('first_name')
                last_name = datas.get('last_name')

                if not self.context.get('userform').is_valid():
                    return self.render_template

                user = User.objects.create_user(
                    username=username, email=email, first_name=first_name,
                    last_name=last_name, password=password
                )
                user.save()
            
                user = auth.authenticate(
                    self.request, username=username, password=password)

                if user:
                    auth.login(self.request, user)
                    messages.success(self.request, 'Usuário criado com sucesso.')
                    return redirect(reverse('produto:lista'))
                else:
                    return redirect(reverse('perfil:login'))

            else:
                user = auth.authenticate(
                    self.request, username=login_username, password=login_password)

                if not self.context.get('loginform').is_valid():
                    return self.render_template

                if user:
                    auth.login(self.request, user)
                    return redirect(reverse('produto:lista'))
                else:
                    messages.error(
                        self.request, "Ocorreu um erro. Tente novamente mais tarde.")
        else:
            if self.context.get('userform').is_valid():
                messages.success(self.request, 'Dados atualizados.')
                user = auth.authenticate(
                    self.request,
                    username=self.context['userform'].cleaned_data.get('username'),
                    password=self.context['userform'].cleaned_data.get('password')
                )
                auth.login(self.request, user) if user else None

                self.request.session['cart'] = self.cart
                self.request.session.save()

                return redirect('perfil:login')
            return self.render_template

    def get(self, *args, **kwargs):

        return self.render_template


class FormLoginRegisterAndUpdateController(BaseUserProfile):
    pass


class Update(BaseUserProfile):
    pass


class Login(View):
    pass


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    
    return redirect('perfil:login')
