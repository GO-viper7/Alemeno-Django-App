# Generated by Django 5.0.1 on 2024-01-15 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0002_rename_custom_id_loan_data_custom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_data',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]