# Generated by Django 4.2.4 on 2023-09-30 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0042_remove_productdisplay_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='weigth',
            new_name='weight',
        ),
    ]
