from django.db import models

class customer_data(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    monthly_salary = models.BigIntegerField()
    phone_number = models.BigIntegerField() 
    approved_limit = models.BigIntegerField()
    
    
class loan_data(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True)
    custom = models.ForeignKey(customer_data, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.BigIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.BigIntegerField()
    date_of_approval = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)
