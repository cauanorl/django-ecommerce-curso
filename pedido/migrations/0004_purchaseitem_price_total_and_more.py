# Generated by Django 4.0.3 on 2022-04-18 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0003_purchase_quantity_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseitem',
            name='price_total',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='promotional_price_total',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]