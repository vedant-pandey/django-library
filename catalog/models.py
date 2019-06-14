from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date

# class MyModelName(models.Model):
#     """A typical class defining model, derived from the Model class."""

#     # Fields
#     my_field_name = models.CharField(max_length,help_text='Enter field documentation')

#     # Metadata
#     class Meta:
#         ordering = ['-my_field_name']
    
#     # Methods
#     def get_absolute_url(self):
#         """Returns the urls to access a particular instance of MyModelName."""
#         return reverse("model-detail-view", args=[str(self.id)])

#     def __str__(self):
#         """String for representing the MyModelName object (in Admin site, etc)."""
#         return self.my_field_name

class Genre(models.Model):
    """Model representing a book genre"""
    name = models.CharField(max_length=200, help_text='Enter a book genre(e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200,help_text='Enter the title of your book')
    isbn = models.CharField('ISBN',max_length=13,help_text='13 character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    summary = models.TextField(max_length=1000,help_text='Enter a brief description of the book')

    # Foriegn Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file. 
    # Strings must be used for reference if model is defined after it is referenced in the file.
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre,help_text='Select a genre for this book')

    # ManyToManyField used because a genre can contain many books and a Book can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin"""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])
    
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular instance of the book.')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank = True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned','Set book as returned'),)
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Models representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField('Deceased', blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
