# Generated by Django 4.2.4 on 2023-12-23 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0107_productsubcategory_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsubcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_mansory_line',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_rope',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('None', 'None'), ('Rope', 'Rope'), ('Lines and yarns', 'Lines and yarns'), ('Mansory Lines', 'Mansory Lines')], default='None', max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
        migrations.DeleteModel(
            name='ProductSubCategory',
        ),
    ]
