# Generated by Django 4.2.4 on 2023-11-17 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0076_order_invoice_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
