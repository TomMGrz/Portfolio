# Generated by Django 4.2.4 on 2023-11-10 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0072_order_invoice_order_is_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_company',
        ),
    ]
