import datetime
import uuid
from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(
        "First Name", max_length=100, help_text="Enter Author's first name.")
    last_name = models.CharField(
        "Last Name", max_length=100, help_text="Enter Author's last name.")
    date_of_birth = models.DateField("Born")
    date_of_death = models.DateField("Died", null=True, blank=True)

    @property
    @admin.display(ordering='last_name', description="Author's Name")
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("author_detail", kwargs={"pk": self.pk})


class Genre(models.Model):
    name = models.CharField("Genre Name", max_length=200,
                            help_text="Enter a book genre (e.g. Science Fiction)")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter a natural language name.")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT)
    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(
        Genre, help_text='Select a genre for this book')
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    LOAN_STATUS = (
        ('a', 'Available'),
        ('m', 'Maintenance'),
        ('r', 'Reserved'),
        ('o', 'On Loan')
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text='Book availability')

    @property
    def is_overdue(self):
        if self.due_back and datetime.date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return self.book.title
