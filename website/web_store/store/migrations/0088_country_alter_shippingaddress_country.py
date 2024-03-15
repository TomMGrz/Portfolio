# Generated by Django 4.2.4 on 2023-12-11 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0087_alter_order_transaction_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=2, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.country'),
        ),
    ]
