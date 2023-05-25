from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from .models import Author
from .forms import AuthorsForm
from .filters import AuthorFilter
from .services import delete_author


class AuthorsList(LoginRequiredMixin, ListView):
    template_name = 'authors/authors_list.html'
    model = Author
    context_object_name = 'authors'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return Author.objects.filter(date_deleted=None)

    def paginate_queryset(self, queryset, page_size):
        self.q_filter = AuthorFilter(self.request.GET, queryset=self.get_queryset())
        return super().paginate_queryset(self.q_filter.qs, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.q_filter
        return context


class AuthorsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('authors.добавление_авторов',)
    template_name = 'authors/authors_create.html'
    model = Author
    context_object_name = 'author'
    form_class = AuthorsForm
    success_url = reverse_lazy('authors')


class AuthorsDetail(LoginRequiredMixin, DetailView):
    template_name = 'authors/authors_detail.html'
    model = Author
    context_object_name = 'author'

    def get_queryset(self):
        return Author.objects.filter(date_deleted=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_link'] = self.get_object().get_delete_url()
        return context


class AuthorsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('authors.изменение_авторов',)
    template_name = 'authors/authors_update.html'
    model = Author
    context_object_name = 'author'
    form_class = AuthorsForm

    def get_success_url(self):
        return self.object.get_detail_url()

    def get_queryset(self):
        return Author.objects.filter(date_deleted=None)


class AuthorsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('authors.удаление_авторов',)
    model = Author
    success_url = reverse_lazy('authors')

    def post(self, request, *args, **kwargs):
        author = self.get_object()
        delete_author(author)
        return HttpResponseRedirect(reverse_lazy('authors'))
