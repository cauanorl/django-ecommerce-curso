# Generated by Django 4.0.3 on 2022-03-21 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(max_length=50, verbose_name='Endereço'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.PositiveIntegerField(verbose_name='Idade'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth_date',
            field=models.DateField(verbose_name='Data de nascimento'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cep',
            field=models.CharField(help_text='Apenas valores numéricos.', max_length=8, verbose_name='CEP'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=30, verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='complement',
            field=models.CharField(max_length=30, verbose_name='Complemento'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cpf',
            field=models.CharField(help_text='Apenas valores numéricos.', max_length=11, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='neighborhood',
            field=models.CharField(max_length=30, verbose_name='Bairro'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='number',
            field=models.CharField(max_length=5, verbose_name='Número'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], default='SP', max_length=2, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]
