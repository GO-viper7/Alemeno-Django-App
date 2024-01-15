from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = customer_data
        fields = ['first_name', 'last_name', 'age', 'monthly_salary', 'phone_number']

class LoanDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = loan_data
        fields = ('id', 'custom', 'loan_amount', 'tenure', 'interest_rate', 'monthly_payment', 'emis_paid_on_time', 'date_of_approval', 'end_date')