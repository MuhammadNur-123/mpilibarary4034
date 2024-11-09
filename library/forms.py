from django import forms
from .models import Loan

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['book', 'member', 'return_date', 'status', 'fine']
class FinePaymentForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['payment_method']  # Only allow selecting payment method
        widgets = {
            'payment_method': forms.RadioSelect(),  # Render payment methods as radio buttons
        }
