# Generated by Django 5.0.3 on 2024-03-09 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_aboutme_image_aboutme_text1_aboutme_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutme',
            name='text1',
        ),
        migrations.AddField(
            model_name='aboutme',
            name='text',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
