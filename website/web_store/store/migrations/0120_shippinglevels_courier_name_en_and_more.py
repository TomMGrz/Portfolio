# Generated by Django 4.2.4 on 2023-12-30 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0119_product_subcategory_en_product_subcategory_pl_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippinglevels',
            name='courier_name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shippinglevels',
            name='courier_name_pl',
            field=models.CharField(max_length=100, null=True),
        ),
    ]