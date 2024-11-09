from django import forms
from .models import Author, Book

from django import forms
from .models import BookCategory

class BookCategoryForm(forms.ModelForm):
    class Meta:
        model = BookCategory
        fields = ['name', 'description']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [ 'image','name', 'bio', 'date_of_birth', 'country']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['image','title', 'author', 'category', 'isbn', 'published_date', 'language', 'available_copies',  'description']
