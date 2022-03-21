# Generated by Django 4.0.3 on 2022-03-21 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Produto', 'verbose_name_plural': 'Produtos'},
        ),
        migrations.AlterModelOptions(
            name='variation',
            options={'verbose_name': 'Variação', 'verbose_name_plural': 'Variações'},
        ),
        migrations.AlterField(
            model_name='variation',
            name='inventory',
            field=models.PositiveBigIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='variation',
            name='price',
            field=models.FloatField(),
        ),
    ]