# Generated by Django 4.2.4 on 2023-12-19 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0096_alter_product_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogitem',
            name='image',
        ),
        migrations.RemoveField(
            model_name='catalogitem',
            name='image1',
        ),
        migrations.RemoveField(
            model_name='catalogitem',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='catalogitem',
            name='image3',
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='catalog_description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]