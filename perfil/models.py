from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

from utils.validacpf import valida_cpf

# Create your models here.
class UserProfile(models.Model):
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    age = models.PositiveIntegerField(verbose_name='Idade')
    birth_date = models.DateField(verbose_name='Data de nascimento')
    cpf = models.CharField(
        max_length=11, help_text='Apenas valores numéricos.', verbose_name='CPF')
    address = models.CharField(max_length=50, verbose_name='Endereço')
    number = models.CharField(max_length=5, verbose_name='Número')
    complement = models.CharField(max_length=30, verbose_name='Complemento')
    neighborhood = models.CharField(max_length=30, verbose_name='Bairro')
    cep = models.CharField(
        max_length=8, help_text='Apenas valores numéricos.', verbose_name='CEP')
    city = models.CharField(max_length=30, verbose_name='Cidade')
    state = models.CharField(
        max_length=2,
        default='SP',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        ),
        verbose_name='Estado',
    )

    def clean(self) -> None:
        errors = {}

        if not valida_cpf(self.cpf):
            errors.update({
                'cpf': 'Número de CPF incorreto, Verifique se o mesmo foi digitado corretamente.',
            })
        
        if len(self.cep) != 8 or not str(self.cep).isnumeric():
            errors.update({
                'cep': 'Campo CEP digitado incorretamente.',
            })
        
        if errors:
            raise ValidationError(errors)

    def __str__(self): return f'{self.user}'
