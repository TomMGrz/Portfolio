# Generated by Django 4.2.4 on 2023-12-20 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0098_productcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdisplay',
            name='material',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]