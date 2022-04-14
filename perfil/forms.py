from django.contrib.auth.models import User
from utils import utils

from django import forms

from django.contrib import auth

from . import models


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ['user']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username',
            'email', 'password', 'repeat_password']
        widgets = {
            'password': forms.PasswordInput()
        }
    
    username = forms.CharField(
        label='Nome de usuário',
        max_length=255,
        required=False,
    )

    password = forms.CharField(
        label='Senha',
        required=False,
        max_length=25,
        widget=forms.PasswordInput(),
        help_text="Senha deve conter minímo de 8 caracteres",
    )
    repeat_password = forms.CharField(
        max_length=25,
        label="Repetir senha",
        required=False,
        widget=forms.PasswordInput(), 
    )

    def __init__(self, user=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.user = user

    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        datas = {
            'first_name': cleaned.get('first_name'),
            'last_name': cleaned.get('last_name'),
            'username': cleaned.get('username'),
            'email': cleaned.get('email'),
            'password': cleaned.get('password'),
            'password2': cleaned.get('repeat_password'),
        }

        # Usuários logados: atualização
        if self.user:
            validation_error_msgs.update(utils.validate_fields(datas, self.user))
            
            if validation_error_msgs:
                raise forms.ValidationError(validation_error_msgs)
            
            user = User.objects.filter(username=self.user.username).first()

            user.username = datas['username']
            user.email = datas['email']
            user.first_name = datas['first_name']
            user.last_name = datas['last_name']

            if datas['password']:
                user.set_password(datas['password'])
            
            user.save()

        # Usuários deslogados: cadastro
        else:
            is_register = [
                item if item != '' else None for item in datas.values()]

            for value in is_register:
                if not value is None:
                    is_register = False
                    break

            if is_register:
                return super().clean(*args, **kwargs)

            validation_error_msgs.update(utils.validate_fields(datas))

            if validation_error_msgs and not datas.get('login_username'):
                raise forms.ValidationError(validation_error_msgs)

        return super().clean(*args, **kwargs)


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['login_username', 'login_password']
    
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
    
    login_username = forms.CharField(
        label='Nome de usuário',
        max_length=255,
        required=False,
    )

    login_password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(),
        required=False,
        max_length=25,
    )

    def clean(self, *args, **kwargs):
        errors = {}

        username = self.cleaned_data.get('login_username')
        password = self.cleaned_data.get('login_password')

        if not username and not password:
            return super().clean(*args, **kwargs)

        if not User.objects.filter(username=username).exists():
            errors.update({'login_username': 'Usuário não existe.'})
            raise forms.ValidationError(errors)
        
        user = auth.authenticate(
            self.request,
            username=username,
            password=password)
        
        if not user:
            raise forms.ValidationError({"login_password": 'Senha está incorreta.'})

        return super().clean(*args, **kwargs)
