from django.urls import path
from . import views

urlpatterns = [
    path('loan/list/', views.loan_list, name='loan_list'),
    path('loan/create/', views.loan_create, name='loan_create'),
    path('loan/update/<int:pk>/', views.loan_update, name='loan_update'),
    path('loan/delete/<int:pk>/', views.loan_delete, name='loan_delete'),
    path('loan/return/<int:loan_id>/', views.return_book, name='return_book'),  # For returning a book
    path('loan/pay_fine/<int:loan_id>/', views.pay_fine, name='pay_fine'),  # For paying fine
   
]
