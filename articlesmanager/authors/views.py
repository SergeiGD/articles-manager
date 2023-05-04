from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
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
    success_url = reverse_lazy('authors')


class AuthorsDetail(DetailView):
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
    success_url = reverse_lazy('authors')

    def get_queryset(self):
        return Author.objects.filter(date_deleted=None)


class AuthorsDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        author = self.get_object()
        author.date_deleted = timezone.now()
        author.save()
        return HttpResponseRedirect(self.get_success_url())
