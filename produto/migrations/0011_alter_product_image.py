# Generated by Django 4.0.3 on 2022-03-29 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0010_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='produto_imagens/%Y/%m/', verbose_name='Imagem'),
        ),
    ]
