# Generated by Django 4.2.4 on 2023-12-20 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0102_remove_catalog_catalog_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='short_description',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
