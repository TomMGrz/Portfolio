# Generated by Django 5.0.3 on 2024-03-09 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_portfoliopage_remove_portfolio_text_field'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PortfolioPage',
        ),
    ]
