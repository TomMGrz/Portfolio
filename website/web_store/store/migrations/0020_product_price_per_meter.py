# Generated by Django 4.2.4 on 2023-09-25 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_rename_weight_product_weigth'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_per_meter',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
