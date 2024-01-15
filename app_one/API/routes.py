from django.urls import path
from . import views 


urlpatterns = [
   path('register/', views.register, name = "Add Customer"),
   path('check-eligibility/', views.check_eligibility, name = "Checks Eligibility for Loan"),
   path('create-loan/', views.create_loan, name = "Create Loan"),
   path('view-loan/<int:loan_id>', views.get_loan_by_id, name = "View Loan By Loan ID"), 
   path('view-loans/<int:customer_id>', views.get_loans_by_customer, name = "View Loans By Customer ID"), 
   
   # Extra routes to display data
   path('customers/', views.get_all_customers, name = "Display Customers"),
   path('loans/', views.get_all_loans, name = "Display Loans"),
]