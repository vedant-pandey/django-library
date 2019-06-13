from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)

class BooksInline(admin.TabularInline):
    model = Book

# Define admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]

# Register the admin class with the assiciated model
admin.site.register(Author, AuthorAdmin)

class BooksInstancesInline(admin.TabularInline):
    model = BookInstance

# Register the admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstancesInline]

# Register the admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back','id')
    list_filter = ('status', 'due_back', 'status')

    fieldsets = (
        (None, {
            "fields": (
                'book',
                'imprint',
                'id'
            ),
        }),
        ('Availability',{
            'fields': ('status', 'due_back')
        }),
    )
    