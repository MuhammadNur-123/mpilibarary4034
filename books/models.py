from django.db import models 
from users.models import User
import pycountry

class Author(models.Model):
    COUNTRY_NAME_CHOICES = [('SL', 'Select Country Name')] + [
    (country.alpha_2, country.name) for country in pycountry.countries
]
   

    image=models.ImageField(
        upload_to='author_image/',
        blank=True,
        null=True
    )
    name= models.CharField(max_length=255)
    bio=models.TextField(blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    country=models.CharField(
        max_length=30,
        choices=COUNTRY_NAME_CHOICES,
        default='SL',
        )
    
    def __str__(self):
        return self.name
   

class BookCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    
class Book(models.Model):
    LANGUAGE_NAME_CHOICES = [
    ('BD', 'Bangla'),
    ('PK', 'Urdu'),
    ('LN', 'Select Book Language'),
    ('IN', 'Hindi'),
    ('EN', 'English'),
    ('FR', 'French'),
    ('ES', 'Spanish'),
    ('DE', 'German'),
    ('CN', 'Mandarin'),
    ('JP', 'Japanese'),
    ('RU', 'Russian'),
    ('IT', 'Italian'),
    ('PT', 'Portuguese'),
    ('AR', 'Arabic'),
    ('KR', 'Korean'),
    ('TR', 'Turkish'),
]
    image = models.ImageField(
        upload_to='book_image/',
        blank=True,
        null=True 
    )
    
    title = models.CharField(max_length=255)
    entry_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, null=True, blank=True)
    isbn = models.CharField(max_length=13)
    published_date = models.DateField()
    language=models.CharField(
        max_length=30,
        choices=LANGUAGE_NAME_CHOICES,
        default='LN',
        )
    available_copies = models.IntegerField()
    
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title