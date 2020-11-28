from django.shortcuts import render, get_object_or_404
from .models import Book
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


# def books_home(request):
#     num_books = Book.objects.all()
#     context = {
#         'num_books': num_books
#     }
#     return render(request, 'Books/books_home.html', context)


class BookListView(ListView):

    context = {
        'books': Book.objects.all()
    }

    model = Book
    template_name = 'experiment/book_home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'books'
    ordering = ['-date_created']
    paginate_by = 1


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book

  

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['name', 'genre', 'image', 'title', 'intro', 'content']
    succes_url = 'book-home'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class BookUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['name', 'genre', 'image', 'title', 'intro', 'content']
    succes_url = 'book-home'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.author:
            return True
        return False



class BookDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Book
    success_url = '/'

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.author:
            return True
        return False



    