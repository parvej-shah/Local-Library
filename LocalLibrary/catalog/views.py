from dataclasses import field
import datetime
from .forms import BookRenewalForm
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from catalog.models import Author, Book, Language, Genre, BookInstance
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.


def index(request):
    num_book = Book.objects.all().count()
    num_author = Author.objects.all().count()
    num_genre = Genre.objects.all().count()
    num_language = Language.objects.all().count()
    num_book_availabe = BookInstance.objects.filter(status='a').count()
    num_copies = BookInstance.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_book': num_book,
        'num_author': num_author,
        'num_language': num_language,
        'num_genre': num_genre,
        'num_book_available': num_book_availabe,
        'num_copies': num_copies,
        'num_visits': num_visits
    }

    return render(request, 'catalog/index.html', context)


class BookListView(ListView):
    model = Book


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # book = Book.objects.get(pk=self.kwargs['pk'])
        # bookinst = BookInstance.objects.get(
        #     book=book)
        context['a'] = [b for b in BookInstance.objects.filter(
            book=Book.objects.get(pk=self.kwargs['pk'])) if b.status == 'a'][:1]
        context['d'] = [e for e in BookInstance.objects.filter(
            book=Book.objects.get(pk=self.kwargs['pk'])).order_by('due_back') if e.due_back and e.due_back < datetime.date.today() + datetime.timedelta(weeks=1)][:1]

        return context


class AuthorListView(ListView):
    model = Author


class AuthorDetailView(DetailView):
    model = Author


class UserBorrowedListView(LoginRequiredMixin, ListView):
    model = BookInstance

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

    template_name = "user/user_borrowed.html"


class Librarian(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BookInstance
    permission_required = 'catalog.view_book'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

    template_name = "user/librarian.html"


@permission_required('catalog.view_book', )
def book_renewal_form(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = BookRenewalForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('librarian'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = BookRenewalForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'user/book_renwal_form.html', context)
