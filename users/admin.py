from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display=('email','name','roll','department','session','phone_number','is_active','is_admin','user_type')
    fields=('email','name','roll','department','session','phone_number','address','membership_number','user_type','image','is_active','is_admin')
    search_fields = ('email', 'name', 'roll', 'department', 'session', 'phone_number', 'membership_number')
    readonly_fields = ('email', 'membership_number')


admin.site.register(User,UserAdmin)