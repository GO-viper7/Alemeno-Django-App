# Generated by Django 5.0.1 on 2024-01-15 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan_data',
            old_name='custom',
            new_name='custom',
        ),
    ]