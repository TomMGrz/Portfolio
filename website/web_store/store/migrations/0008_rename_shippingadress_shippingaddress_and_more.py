# Generated by Django 4.2.4 on 2023-09-03 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_orderitem_total_price'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShippingAdress',
            new_name='ShippingAddress',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='adress',
            new_name='address',
        ),
    ]
