# Generated by Django 4.2.4 on 2023-08-28 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_order_alter_customer_user_shippingadress_orderitem_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.IntegerField(null=True),
        ),
    ]
