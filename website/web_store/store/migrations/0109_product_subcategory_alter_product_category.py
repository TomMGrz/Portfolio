# Generated by Django 4.2.4 on 2023-12-23 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0108_remove_productsubcategory_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('All', 'All'), ('Rope', 'Rope'), ('Lines and yarns', 'Lines and yarns'), ('Mansory Lines', 'Mansory Lines')], default='None', max_length=100, null=True),
        ),
    ]