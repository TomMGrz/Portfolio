# Generated by Django 4.2.4 on 2024-01-04 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0127_delete_returnitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_id', models.CharField(blank=True, max_length=6, null=True)),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('reason', models.CharField(max_length=500)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=100)),
                ('adding_date', models.DateTimeField(auto_now_add=True)),
                ('confirmed', models.BooleanField(default=False, null=True)),
                ('complete', models.BooleanField(default=False, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.order')),
            ],
        ),
        migrations.CreateModel(
            name='ReturnItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
                ('return_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='return_items', to='store.returnrequest')),
            ],
        ),
    ]
