from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from . import serializers
from . import models
from .utilities import *
import random
from django.shortcuts import get_object_or_404



@api_view(['GET'])
def get_all_customers(request):
    try:
        customers = models.customer_data.objects.all()
        serializer = serializers.CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
@api_view(['GET'])
def get_all_loans(request):
    try:
        loans = models.loan_data.objects.all()
        serializer = serializers.LoanDataSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['POST'])
def register(request):
  serializer = serializers.CustomerSerializer(data=request.data)

  if serializer.is_valid():
    
    monthly_salary = serializer.validated_data['monthly_salary']
    approved_limit = round(36 * monthly_salary / 100000) * 100000
    serializer.validated_data['approved_limit'] = approved_limit
    highest_id = models.customer_data.objects.order_by('-id').first().id or 0
    new_id = int(highest_id) + 1
    serializer.validated_data['id'] = str(new_id)
    customer = serializer.save()
    response_data = {
            'message': 'Customer registered successfully',
            'customer': {
                'id': customer.id,
                'Name': f'{customer.first_name} {customer.last_name}',
                'age': customer.age,
                'monthly_salary': customer.monthly_salary,
                'phone_number': customer.phone_number,
                'approved_limit': customer.approved_limit,
            }
    }
    return Response({'data': response_data}, status=status.HTTP_201_CREATED)
  
  else:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
@api_view(['POST'])
def check_eligibility(request):
    try:
        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        tenure = request.data.get('tenure')
        
        
        customer = models.customer_data.objects.get(id=customer_id)
        current_loans = models.loan_data.objects.filter(custom_id=customer_id)
        
        credit_score = calculate_credit_score(customer, current_loans)
        print('credit_score : ', credit_score)
        current_loans_sum = current_loans.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0
        approval, corrected_interest_rate = determine_loan_approval(credit_score, interest_rate, current_loans_sum, customer.monthly_salary)


        response_data = {
            'customer_id': customer.id,
            'approval': approval,
            'interest_rate': interest_rate,
            'corrected_interest_rate': corrected_interest_rate,
            'tenure': tenure,
            'monthly_installments': calculate_monthly_installments(loan_amount, corrected_interest_rate, tenure),
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except models.customer_data.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['POST'])
def create_loan(request):
    try:
        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        tenure = request.data.get('tenure')
        
        
        customer = models.customer_data.objects.get(id=customer_id)
        current_loans = models.loan_data.objects.filter(custom_id=customer_id)
        
        credit_score = calculate_credit_score(customer, current_loans)
        print('credit_score : ', credit_score)
        current_loans_sum = current_loans.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0
        approval, corrected_interest_rate = determine_loan_approval(credit_score, interest_rate, current_loans_sum, customer.monthly_salary)
        
        new_loan = {
            "id" : random.randint(10000, 99999),
            "custom" : str(customer.id),
            "loan_amount" : str(loan_amount),
            "tenure" : tenure, 
            "interest_rate" : str(corrected_interest_rate),
            "monthly_payment" : str(round(calculate_monthly_installments(loan_amount, corrected_interest_rate, tenure),2)),
            "emis_paid_on_time" : 0,
            "date_of_approval" : "XXXX",
            "end_date" : "XXXX"
        }
        print(new_loan)
        serializer = serializers.LoanDataSerializer(data=new_loan)
        response_data = {
            'customer_id': customer.id,
            'loan_approved': approval,
            'monthly_installments': calculate_monthly_installments(loan_amount, corrected_interest_rate, tenure),
        }
        if serializer.is_valid():
            if(approval == True): 
                loan = serializer.save()
                response_data = {
                    'id': loan.id,
                    'customer_id': customer.id,
                    'loan_approved': approval,
                    'monthly_installments': calculate_monthly_installments(loan_amount, corrected_interest_rate, tenure),
                }
                response_data['message'] = "Your Loan Approval has been accepted"
            else :  
                response_data['message'] = "Your Loan Approval has been rejected"
            return Response(response_data, status=status.HTTP_200_OK)
        else : 
            print(serializer.errors)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except models.customer_data.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


  
@api_view(['GET'])
def get_loan_by_id(request, loan_id):
    loan_data = get_object_or_404(models.loan_data, id=loan_id)
    loan_serializer = serializers.LoanDataSerializer(loan_data)
    customer_serializer = serializers.CustomerSerializer(loan_data.custom)
    response_data = {
        "loan_details": loan_serializer.data,
        "customer_details": customer_serializer.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)
    
    
@api_view(['GET'])
def get_loans_by_customer(request, customer_id):
    loans_data = loan_data.objects.filter(custom_id=customer_id)
    if not loans_data:
        return Response({"error": "No loans found for the customer"}, status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.LoanDataSerializer(loans_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)