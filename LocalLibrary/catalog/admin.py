from django.contrib import admin
from .models import Author, Book, BookInstance, Language, Genre
# Register your models here.
# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Language)
# admin.site.register(Genre)


class BookInline(admin.TabularInline):
    model = Book
    fields = ('title', 'summary', 'language')
    extra = 0


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    inlines = [BookInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'date_of_birth', 'date_of_death']
    fields = ('first_name', 'last_name', ('date_of_birth', 'date_of_death'))
    list_filter = ('date_of_birth', 'date_of_death',)
    inlines = (BookInline,)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'display_genre', 'language', 'isbn']
    inlines = (BookInstanceInline,)

    def display_genre(self, obj):
        return ", ".join([a.name for a in obj.genre.all()])


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'borrower', 'id', 'status', 'due_back']
    fieldsets = (
        (None, {
            "fields": (
                'id', 'book', 'imprint', 'borrower'
            ),
        }),
        ('Availability', {
            "fields": (
                ('status', 'due_back'),
            ),
        }),
    )


class BookInlines(admin.TabularInline):
    model = Book.genre.through
    list_display = ['title']
    extra = 0


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    inlines = [BookInlines, ]
