# Generated by Django 4.2.4 on 2023-09-27 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_alter_product_length_delete_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='length',
        ),
    ]