from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

admin.site.register(Genre)
admin.site.register(Language)

#Book inline 
class BookInline(admin.TabularInline):
    model = Book

# admin.site.register(Author)
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
# admin.site.register(Book)
# admin.site.register(BookInstance)
# Register the Admin classes for Book using the decorator

#InlineModelAdmin: add information linking directly in the same interface
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]
# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    #List view
    list_display = ('status', 'due_back','id')
    #Create filter
    list_filter = ('status', 'due_back')
    #Group the related fields for different sections
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )