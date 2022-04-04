
from django.contrib.auth.models import User
from utils import utils

from django import forms


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
            if datas['username'] == self.user.username:
                validation_error_msgs.update(utils.validate_fields(datas))
        # Usuários deslogados: cadastro
        else:
            pass
        
        if validation_error_msgs:
            raise forms.ValidationError(validation_error_msgs)
        
        return super().clean(*args, **kwargs)
