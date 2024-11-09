from django.urls import path , include
from . import views

from .views import create_user, update_user, delete_user, all_users ,profile_view

urlpatterns=[
    path('', create_user, name='create_user'), 
    path('profile/', profile_view, name='profile_view'),
    path('update_user_status/<int:user_id>/', views.update_user_status, name='update_user_status'),
    path('update/<int:user_id>/', update_user, name='update_user'),  # URL for user update
    path('delete/<int:user_id>/', delete_user, name='delete_user'),  # URL for user deletion
    path('list/', all_users, name='all_users'),  # URL for listing all users
]