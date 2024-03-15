# Generated by Django 4.2.4 on 2023-08-29 11:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_image_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.DecimalValidator(8, 2)]),
        ),
    ]
