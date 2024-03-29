# Generated by Django 4.2.4 on 2023-11-10 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0071_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.invoiceinfo'),
        ),
        migrations.AddField(
            model_name='order',
            name='is_company',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
