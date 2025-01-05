from django.db import models

# Create your models here.
# To generate URLS by reversing URL patterns
#Instead of hardcoding URLs in the app, REVERSE allows you to create URLs based on 
#the name of the view and any arguments required for the URL pattern
from django.urls import reverse  
#UniqueConstraint: ensure the uniqueness of the fields in a model
from django.db.models import UniqueConstraint
#case_insentive uniqueness: make the constraint case-insentive which means the filter
#will process English, english, EnGlisH as a same result as english
from django.db.models.functions import Lower
#models.Model
#Base class: Provides all the functionality required for a Django model, including field definitions, querying methods, and database interactions.
#When you define a model, Django:
#Automatically creates a table in the database (when migrations are applied).
#Maps Python code to the underlying database table.
class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    """Common parameter for CharField:
        max_length: maximum number of characters that can be stored in this field
            name = models.CharField(max_length=50)
        default: specify a default value for the field
            status = models.CharField(max_lenth=10, default="active")
        unique: ensure each value in the column is unique across all rows in the database table
            username = models.CharField(max_length=150, unique=True)
        null: determines whether the field can store NULL values in the database
            middle_name= models.CharField(max_length=50, null=True)
        blank: controls whether the field is allowe to be left blank in forms
            nickname = models.CharField(max_lenth=150, blank=True)
        choices: defines a fixed set of valid options for the field as a list of tuples
            Category_choices = [
                ('F','Fiction'),
                ('NF','Non-Fiction'),
                ]
        category = models.CharField(max_length=2, choices=Category_choices)
        help_text: provides a decriptive label for the field, often displayed in forms
            title = models.CharField(max_length=100, help_text='Enter the Book title')   
        verbose_name: provide a human-readable name for the field
            title = models.CharField(max_length=200, verbose_name="Book Title")
        db_index: creates a database index for the field to improve query performance
            email = models.CharField(max_length=100, db_index=True)
        primary_key: makes the field the primary key for the model
            id = models.CharField(max_length=20, primary_key=True)
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])
        #if the id is 5, this method will return the URL: /genres/5/
        """check urls.py file for the patterns
            urlpatterns = [
                path('genres/<int:pk>/', views.GenreDetailView.as_view(), name = "genre-detail"),
                ]
            check views.py, template.py
        """
    #class Meta is an inner class defined within a model class is used to provide metadata about the model
    #specify model-level metadata, such as: constraint, ordering, table names, etc.
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books.
    # Used for one-to-many relationship
    """ models.ForeignKey(to, on_delete, **options)
            to: the target model the ForeignKey points to
            on_delete: specified the behaviour when the referenced object is deleted
                models.CASCADE: delete all the related objects
                models.PROTECT: prevent deletion of the referenced object
                models.SET_NULL: set the foreign key to NULL (requires null=True)
                models.SET_DEFAULT: set the foreign key to its default value (requires default to be specified)
                models.RESTRICT: prevent deletion if referenced
            others: null, blank, default, db_index, unique

    """ 
    # Author as a string rather than object because it hasn't been declared yet in file.
    #CharField: for short text data with a known maximum lenth, requires max_length, stores data as VARCHAR in the database
    #TextField: for longer, free-form text like descriptions, comments, or content, no max_length is needed, stores data as TEXT in the database
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book")
    #isbn: international standard book number, a unique identifier for books
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book")
    # ManyToManyField used because a genre can contain many books and a Book can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    #ManyToManyField relatively has the same parameters as ForeignKey
    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True)

    
    class Meta:
        ordering = ['title', 'author']

    #how genres will be displayed following to the book
    """
        self.genre.all(): fetches all related Genre objects for the current Book instance
        genre.name for genre in self.genre.all()[:3]: iterates through the first 3 Genre objects and extracts their names
        ', '.join(): joins the names into a single string, separated by commas
    """
    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
        #Result of the book has genres: Science, Fantasy, Adventure, the method will return: "Science, Fantasy, Adventure"
    #??? 
    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """Returns the url to access a particular book record."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title


import uuid  # Required for unique book instances
from datetime import date

#???
from django.conf import settings  # Required to assign User as a borrower


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('bookinstance-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'