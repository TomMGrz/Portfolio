# Generated by Django 4.2.4 on 2023-09-11 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_customer_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
    ]
