# Generated by Django 4.2.4 on 2023-12-18 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0090_invoiceinfo_city_invoiceinfo_country_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='invoice_pdf',
            new_name='invoice',
        ),
    ]
