# Generated by Django 4.0.3 on 2022-03-29 18:31

from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0009_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default=pathlib.PureWindowsPath('C:/Users/win/workspace/django-ecommerce-curso/media/sem-foto.jpg'), upload_to='produto_imagens/%Y/%m/', verbose_name='Imagem'),
        ),
    ]