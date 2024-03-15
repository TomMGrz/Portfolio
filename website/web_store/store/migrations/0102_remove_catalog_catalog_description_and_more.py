# Generated by Django 4.2.4 on 2023-12-20 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0101_catalog_image_catalog_image2_catalog_image3_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalog',
            name='catalog_description',
        ),
        migrations.AddField(
            model_name='catalog',
            name='detailed_description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='catalog',
            name='short_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
