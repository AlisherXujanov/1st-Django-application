from typing import List
from users.views import register
from django.shortcuts import render, redirect
from .models import Book, Task
from .forms import TaskForm
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)


class BookListView(ListView):

    context = {
        'books': Book.objects.all()
    }
    model = Book
    template_name = 'experiment/book_home.html'  # <app>/<model>_<viewtype>.html
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


# <<<<<<<<<--------<<<<<<<<---------------<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Vue Beginning
class TaskView(ListView):
    Task.objects.all().delete()

    def get(self, request):
        tasks = list(Task.objects.values())
        if request.is_ajax():
            return JsonResponse({'tasks': tasks}, status=200)

        return render(request, 'experiment/vueTest.html')

    def post(self, request):
        bound_form = TaskForm(request.POST)

        if bound_form.is_valid():
            new_task = bound_form.save()
            return JsonResponse({'task': model_to_dict(new_task)}, status=200)

        return redirect('vueTest')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['tasks'] = Task.objects.all()
        return context_data


# class BaseView(ListView):
#     model = Task
#     context = {
#         "tasks": Task.objects.all()
#     }
#     context_object_name = 'tasks'
#     template_name = 'experiment/vueTest.html'
