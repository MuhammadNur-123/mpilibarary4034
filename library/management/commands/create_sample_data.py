from django.core.management.base import BaseCommand
from books.models import Author, BookCategory, Book  # Update with your app name
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate authors, categories, and books'

    def handle(self, *args, **kwargs):
        # Create authors
        authors = [
            {'name': 'Andrew S. Tanenbaum', 'bio': 'Computer scientist known for his work on operating systems.', 'date_of_birth': '1944-03-16'},
            {'name': 'Donald Knuth', 'bio': 'American computer scientist and mathematician.', 'date_of_birth': '1938-01-10'},
            {'name': 'Robert Sedgewick', 'bio': 'Computer scientist and author of many algorithms books.', 'date_of_birth': '1946-04-20'},
            {'name': 'Simon Haykin', 'bio': 'Known for his work in adaptive filtering and signal processing.', 'date_of_birth': '1938-01-01'},
            {'name': 'Thomas Piketty', 'bio': 'French economist known for his work on wealth distribution.', 'date_of_birth': '1971-05-07'}
        ]

        for author_data in authors:
            author = Author.objects.create(**author_data)

        # Create categories
        categories = [
            {'name': 'Computer Science', 'description': 'Books related to computer science and programming.'},
            {'name': 'Electrical Engineering', 'description': 'Books related to electrical and electronic engineering.'},
            {'name': 'Economics', 'description': 'Books related to economics and finance.'},
            {'name': 'Algorithms', 'description': 'Books specifically about algorithms and data structures.'},
        ]

        for category_data in categories:
            category = BookCategory.objects.create(**category_data)

        # Create books (as examples)
        books = [
            {
                'title': 'Operating Systems: Three Easy Pieces',
                'author': Author.objects.get(name='Andrew S. Tanenbaum'),
                'category': BookCategory.objects.get(name='Computer Science'),
                'isbn': '978-0999209753',
                'published_date': '2018-07-01',
                'available_copies': 5,
                'description': 'An introduction to operating systems concepts.',
            },
            {
                'title': 'The Art of Computer Programming',
                'author': Author.objects.get(name='Donald Knuth'),
                'category': BookCategory.objects.get(name='Algorithms'),
                'isbn': '978-0201896831',
                'published_date': '1997-01-01',
                'available_copies': 3,
                'description': 'Comprehensive guide to algorithms.',
            },
            {
                'title': 'Algorithms',
                'author': Author.objects.get(name='Robert Sedgewick'),
                'category': BookCategory.objects.get(name='Algorithms'),
                'isbn': '978-0321573513',
                'published_date': '2011-10-29',
                'available_copies': 10,
                'description': 'A modern introduction to algorithms.',
            },
            {
                'title': 'Adaptive Filter Theory',
                'author': Author.objects.get(name='Simon Haykin'),
                'category': BookCategory.objects.get(name='Electrical Engineering'),
                'isbn': '978-0132450063',
                'published_date': '2013-01-01',
                'available_copies': 4,
                'description': 'A comprehensive overview of adaptive filtering.',
            },
            {
                'title': 'Capital in the Twenty-First Century',
                'author': Author.objects.get(name='Thomas Piketty'),
                'category': BookCategory.objects.get(name='Economics'),
                'isbn': '978-0674430006',
                'published_date': '2014-04-15',
                'available_copies': 6,
                'description': 'An analysis of wealth and income inequality.',
            },
        ]

        for book_data in books:
            Book.objects.create(**book_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated authors, categories, and books.'))
