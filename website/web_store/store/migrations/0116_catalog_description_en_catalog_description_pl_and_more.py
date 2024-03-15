# Generated by Django 4.2.4 on 2023-12-29 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0115_product_color_en_product_color_pl_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='description_en',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='catalog',
            name='description_pl',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='catalog',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='catalog',
            name='name_pl',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='countries',
            name='name_en',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='countries',
            name='name_pl',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='productdisplay',
            name='color_en',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='productdisplay',
            name='color_pl',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='productdisplay',
            name='material_en',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='productdisplay',
            name='material_pl',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='productdisplay',
            name='name_en',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='productdisplay',
            name='name_pl',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='name_en',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='name_pl',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='subcategory_en',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='subcategory_pl',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
