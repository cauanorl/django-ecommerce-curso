# Generated by Django 4.0.3 on 2022-03-25 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0006_rename_type_product_product_variations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='inventory',
            new_name='stock',
        ),
    ]