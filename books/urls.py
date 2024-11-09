from django.urls import path
from . import views

urlpatterns = [
    path('book_list/', views.book_list, name='book_list'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/add/', views.add_author, name='add_author'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('books/add/', views.add_book, name='add_book'),
    path('edit/<int:pk>/', views.edit_book, name='edit_book'),  # Ensure this pattern exists
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),  
    path('author/edit/<int:pk>/', views.edit_author, name='edit_author'),  # Edit author URL pattern
    path('author/delete/<int:pk>/', views.delete_author, name='delete_author'),  # Delete author URL pattern
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

]   
