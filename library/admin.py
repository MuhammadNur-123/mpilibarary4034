from django.contrib import admin
from .models import Loan

class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'loan_date', 'return_date', 'fine', 'payment_status', 'payment_method')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('book__title', 'member__username')

admin.site.register(Loan, LoanAdmin)
