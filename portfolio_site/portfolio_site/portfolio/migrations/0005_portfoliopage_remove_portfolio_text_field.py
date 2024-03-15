# Generated by Django 5.0.3 on 2024-03-09 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_aboutme_portfolio_text_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_field', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='text_field',
        ),
    ]