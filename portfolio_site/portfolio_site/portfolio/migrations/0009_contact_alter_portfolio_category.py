# Generated by Django 5.0.3 on 2024-03-10 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_remove_aboutme_text1_aboutme_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('facebook_link', models.CharField(blank=True, max_length=100, null=True)),
                ('instagram_link', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='category',
            field=models.CharField(blank=True, choices=[('Artykuły', 'Artykuły'), ('Projekty ze studiów', 'Projekty ze studiów'), ('Inne', 'Inne')], default=None, max_length=100, null=True),
        ),
    ]
