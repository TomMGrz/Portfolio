# Generated by Django 4.2.4 on 2023-09-11 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_remove_customer_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='second_name',
            new_name='last_name',
        ),
    ]