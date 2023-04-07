from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from .models import Author
from .forms import AuthorsForm

class AuthorsList(ListView):
    template_name = 'authors/authors_list.html'
    model = Author
    context_object_name = 'authors'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return Author.objects.filter(date_deleted=None)


class AuthorsCreate(CreateView):
    template_name = 'authors/authors_create.html'
    model = Author
    context_object_name = 'author'
    form_class = AuthorsForm


class AuthorsDetail(DeleteView):
    template_name = 'authors/authors_detail.html'
    model = Author
    context_object_name = 'author'

    def get_queryset(self):
        return Author.objects.filter(date_deleted=None)


class AuthorsUpdate(UpdateView):
    template_name = 'authors/authors_update.html'
    model = Author
    context_object_name = 'author'
    form_class = AuthorsForm

    def get_queryset(self):
        return Author.objects.filter(date_deleted=None)


def delete_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    author.date_deleted = timezone.now()
    author.save()
    return redirect('authors')
