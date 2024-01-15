from django.db.models import Sum, Count, Case, When, FloatField
from .models import customer_data, loan_data

def calculate_credit_score(customer, current_loans):
  approved_limit = customer.approved_limit
  current_loans_sum = current_loans.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0
  #print(current_loans_sum, approved_limit)
  if current_loans_sum > approved_limit:
      return 0 
  else : 
    W1 = 0.3  
    W2 = 0.2 
    W3 = 0.2  
    W4 = 0.3 

    max_possible_percentage = 100
    max_possible_loans = 10
    max_possible_activity = 100000  
    max_possible_volume = 1000000  
    
    past_loans_paid_on_time = loan_data.objects.filter(
        custom=customer.id
       # paid_status=True         I could filter with this, if there's a field called loan_Paid_Status
    ).count() / loan_data.objects.filter(custom_id=customer.id).count()
    score1 = W1 * (past_loans_paid_on_time / max_possible_percentage) * 100
    
    
    number_of_loans_taken = loan_data.objects.filter(custom_id=customer.id).count()
    score2 = W2 * (number_of_loans_taken / max_possible_loans) * 100
    
    
    loan_activity_current_year = loan_data.objects.filter(
        custom_id=customer,
    ).aggregate(
        total_loan_activity=Count('id')
    )['total_loan_activity']
    score3 = W3 * (loan_activity_current_year / max_possible_activity) * 100


    score4 = W4 * (int(current_loans_sum) / max_possible_volume) * 100
    final_score = score1 + score2 + score3 + score4
    
    return final_score
  
  
  
def determine_loan_approval(credit_rating, interest_rate, current_emis, monthly_salary):

    if credit_rating > 50:
        approval_status = True
    elif 50 > credit_rating > 30 and interest_rate > 12:
        approval_status = True
    elif 30 > credit_rating > 10 and interest_rate > 16:
        approval_status = True
    else:
        approval_status = False

    if current_emis > 0.5 * monthly_salary:
        approval_status = False


    corrected_interest_rate = min(interest_rate, 16) 

    return approval_status, corrected_interest_rate

  
def calculate_monthly_installments(loan_amount, corrected_interest_rate, tenure):
    monthly_interest_rate = corrected_interest_rate / 12 / 100
    emi_numerator = loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure
    emi_denominator = (1 + monthly_interest_rate) ** tenure - 1
    emi = emi_numerator / emi_denominator
    return emi
