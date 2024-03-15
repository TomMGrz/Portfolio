# Generated by Django 4.2.4 on 2023-09-28 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0034_rename_product_name_productname_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True)),
                ('product_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productname')),
            ],
        ),
    ]