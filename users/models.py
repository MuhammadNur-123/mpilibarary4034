from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=True):
        """
        Creates and saves a User with the given email, name, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name, and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            name=name
        )
        user.is_admin = True
        user.is_active = True
        
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    USER_TYPE_CHOICES = [
        ('MEM', 'Member'),
        ('LIB', 'Librarian'),
        ('ADM', 'Admin'),
    ]
    USER_TYPE_CHOICES1 = [
        ('CMT', 'Computer Technology'),
        ('ENT', 'Electronics Technology'),
        ('RAC', 'Refrigeration and Air Conditioning Technology'),
        ('FD', 'Food Technology'),
    ]
    image = models.ImageField(upload_to='user_image/', blank=True, null=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    name = models.CharField(max_length=50, blank=True)
    roll = models.PositiveIntegerField(default=0)
    department = models.CharField(max_length=8, choices=USER_TYPE_CHOICES1, default='CMT')
    session = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    membership_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    user_type = models.CharField(max_length=3, choices=USER_TYPE_CHOICES, default='MEM')
   
   
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)




  

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def generate_unique_membership_number(self):
        """
        Generates a unique membership number.
        """
        while True:
            membership_number = f'{uuid.uuid4().hex[:8].upper()}'
            if not User.objects.filter(membership_number=membership_number).exists():
                return membership_number

    def save(self, *args, **kwargs):
        if not self.membership_number:
            self.membership_number = self.generate_unique_membership_number()
        super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
# models.py


class User1(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll = models.IntegerField()
    department = models.CharField(max_length=15, choices=[('CMT', 'Computer Technology'), ('ENT', 'Electronics Technology'),
        ('RAC', 'Refrigeration and Air Conditioning Technology'),
        ('FD', 'Food Technology')])
    session = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    user_type = models.CharField(max_length=3, choices=[('MEM', 'Member'),
     ('LIB', 'Librarian'), ('ADM', 'Admin')])
    image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.name
