# Generated by Django 4.2.4 on 2024-01-05 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0129_returnrequest_encrypted_bank_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='returnrequest',
            old_name='encrypted_bank_account',
            new_name='bank_account',
        ),
    ]