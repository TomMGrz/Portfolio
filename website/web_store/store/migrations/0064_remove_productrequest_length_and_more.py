# Generated by Django 4.2.4 on 2023-11-06 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0063_requestitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productrequest',
            name='length',
        ),
        migrations.RemoveField(
            model_name='productrequest',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productrequest',
            name='quantity',
        ),
    ]
