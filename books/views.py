from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Book, BookCategory
from .forms import AuthorForm, BookForm ,BookCategoryForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'books/author_list.html', {'authors': authors})

@login_required(login_url='/login/')
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'books/author_detail.html', {'author': author})

@login_required(login_url='/login/')
def add_author(request):
    
    if request.method == "POST":
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'books/author_form.html', {'form': form})

@login_required(login_url='/login/')
def edit_author(request, pk):
    
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')  # Replace with the actual list view for authors
    else:
        form = AuthorForm(instance=author)
    return render(request, 'books/edit_author.html', {'form': form, 'author': author})
@login_required(login_url='/login/')
def delete_author(request, pk):
    
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        author.delete()
        return redirect('author_list')  # Replace with the actual list view for authors
    return render(request, 'books/author_delete_confirm.html', {'author': author})


@login_required(login_url='/login/')
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

@login_required(login_url='/login/')
def add_book(request):
    
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})
@login_required(login_url='/login/')
def edit_book(request, pk):
    
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})

@login_required(login_url='/login/')
def delete_book(request, pk):
    
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Assuming 'book_list' is the name of the list view
    return render(request, 'books/delete_confirm.html', {'book': book})




# List all categories
@login_required(login_url='/login/')
def category_list(request):
    categories = BookCategory.objects.all()
    return render(request, 'books/category_list.html', {'categories': categories})

# Create a new category
@login_required(login_url='/login/')
def category_create(request):
    
    if request.method == 'POST':
        form = BookCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = BookCategoryForm()
    return render(request, 'books/category_form.html', {'form': form, 'action': 'Create'})

# Update an existing category
@login_required(login_url='/login/')
def category_update(request, pk):
    
    category = get_object_or_404(BookCategory, pk=pk)
    if request.method == 'POST':
        form = BookCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = BookCategoryForm(instance=category)
    return render(request, 'books/category_form.html', {'form': form, 'action': 'Update'})

# Delete a category
@login_required(login_url='/login/')
def category_delete(request, pk):
    
    category = get_object_or_404(BookCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'books/category_confirm_delete.html', {'category': category})