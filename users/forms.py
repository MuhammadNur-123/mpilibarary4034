from django import forms
from .models import User
from .models import User1

class UserForm1(forms.ModelForm):
    class Meta:
        model = User1
        fields = ['name', 'email', 'roll', 'department', 'session', 'phone_number', 'address', 'user_type', 'image']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'image',
            'name', 
            'email', 
            'roll', 
            'department', 
            'session', 
            'phone_number', 
            'address', 
            'user_type',
            'password' 
            
        ]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'roll': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter roll number'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'session': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter session'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            
        }

    # Additional validations if needed
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
