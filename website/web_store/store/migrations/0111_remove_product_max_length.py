# Generated by Django 4.2.4 on 2023-12-23 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0110_productdisplay_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='max_length',
        ),
    ]
