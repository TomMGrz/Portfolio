# Generated by Django 4.2.4 on 2023-11-07 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0068_rename_invoiceinformation_invoiceinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceinfo',
            name='firm',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]