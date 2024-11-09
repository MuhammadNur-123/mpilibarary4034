
from django.db import models

from books.models import Book
from users.models import User

class Loan(models.Model):
    LOAN_STATUS = [
        ('Borrowed', 'Borrowed'),
        ('Returned', 'Returned'),
    ]
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Nogot', 'Nogot'),
        ('Bkash', 'Bkash'),
        ('Rocket', 'Rocket'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=LOAN_STATUS, default='Borrowed')
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    
    # New fields for payment information
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} - {self.book.title}"

    # Method to calculate fine (e.g., $5 per day late)
    def calculate_fine(self):
        if self.return_date and self.return_date > self.loan_date:
            days_late = (self.return_date - self.loan_date).days
            if days_late > 0:
                self.fine = days_late * 5.00  # Example: $5 per day late
            else:
                self.fine = 0.00
        self.save()


