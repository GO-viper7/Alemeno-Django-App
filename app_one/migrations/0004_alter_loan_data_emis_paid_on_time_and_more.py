# Generated by Django 5.0.1 on 2024-01-15 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0003_alter_customer_data_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan_data',
            name='emis_paid_on_time',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='loan_data',
            name='tenure',
            field=models.BigIntegerField(),
        ),
    ]