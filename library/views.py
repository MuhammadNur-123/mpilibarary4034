from django.shortcuts import render, get_object_or_404, redirect
from .models import Loan
from .forms import LoanForm
from django.contrib.auth.decorators import login_required
from .forms import FinePaymentForm
from django.utils import timezone
from django.contrib import messages
from datetime import datetime



@login_required(login_url='/login/')
def loan_list(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    loans = Loan.objects.all()
    return render(request, 'loans/loan_list.html', {'loans': loans})
@login_required(login_url='/login/')
def loan_create(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loan_list')
    else:
        form = LoanForm()
    return render(request, 'loans/loan_form.html', {'form': form})
@login_required(login_url='/login/')
def loan_update(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)
        if form.is_valid():
            form.save()
            return redirect('loan_list')
    else:
        form = LoanForm(instance=loan)
    return render(request, 'loans/loan_form.html', {'form': form})

@login_required(login_url='/login/')
def loan_delete(request, pk):
    if not request.user.is_staff:
        return redirect('loan_list')
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        loan.delete()
        return redirect('loan_list')
    return render(request, 'loans/loan_confirm_delete.html', {'loan': loan})

@login_required
def return_book(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    # If the book is already returned, redirect back to loan list
    if loan.status == 'Returned':
        messages.warning(request, "This book has already been returned.")
        return redirect('loan_list')

    # Set return date and calculate fine
    loan.return_date = timezone.now()
    loan.status = 'Returned'
    loan.calculate_fine()  # This will calculate the fine based on late return
    loan.save()

    # Redirect to payment page if fine is applicable
    if loan.fine > 0:
        messages.info(request, f"You have a fine of ${loan.fine}. Please complete the payment.")
        return redirect('pay_fine', loan_id=loan.id)
    else:
        messages.success(request, "Book returned successfully!")
        return redirect('loan_list')

@login_required
def pay_fine(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    # Ensure the book has been returned before making payment
    if loan.status != 'Returned':
        messages.warning(request, "You cannot pay a fine for a book that hasn't been returned.")
        return redirect('loan_list')

    if request.method == 'POST':
        form = FinePaymentForm(request.POST, instance=loan)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.payment_status = True
            loan.payment_date = timezone.now()
            loan.save()
            messages.success(request, "Fine payment successful.")
            return redirect('loan_list')
    else:
        form = FinePaymentForm(instance=loan)

    return render(request, 'loans/pay_fine.html', {'loan': loan, 'form': form})


def calculate_fine(self):
    # Assuming `due_date` is a date and `return_date` is a datetime
    if isinstance(self.return_date, datetime.datetime):
        return_date = self.return_date.date()  # Convert datetime to date

    if return_date > self.due_date:
        # Calculate fine logic here
        fine = (return_date - self.due_date).days * self.fine_rate
        return fine
    return 0
