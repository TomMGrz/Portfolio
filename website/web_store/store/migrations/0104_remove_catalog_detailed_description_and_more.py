# Generated by Django 4.2.4 on 2023-12-21 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0103_alter_catalog_short_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalog',
            name='detailed_description',
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='short_description',
        ),
        migrations.AddField(
            model_name='catalog',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]