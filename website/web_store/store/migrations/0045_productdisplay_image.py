# Generated by Django 4.2.4 on 2023-09-30 11:32

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0044_remove_productdisplay_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdisplay',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name=store.models.Image),
        ),
    ]
