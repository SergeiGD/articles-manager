from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.core.paginator import Paginator
from .models import Article, ArticleState
from authors.models import Author
from users.models import CustomUser
from states.models import State
from .forms import ArticlesForm
from notifications.services import create_reviewer_notification
from .filters import ArticleFilter
from authors.filters import AuthorFilter
from users.filters import CustomUserFilter
from users.services import can_create_review
from . import services



class ArticlesList(LoginRequiredMixin, ListView):
    template_name = 'articles/articles_list.html'
    model = Article
    context_object_name = 'articles'
    paginator_class = Paginator
    paginate_by = 8

    def paginate_queryset(self, queryset, page_size):
        self.q_filter = ArticleFilter(self.request.GET, queryset=self.get_queryset())
        return super().paginate_queryset(self.q_filter.qs, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.q_filter
        return context

    def get_queryset(self):
        return Article.objects.filter(date_deleted=None)


class ArticlesDetail(LoginRequiredMixin, DetailView):
    template_name = 'articles/articles_detail.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_create_review'] = can_create_review(self.request.user, self.object)
        context['delete_link'] = self.get_object().get_delete_url()
        context['is_enable_for_voting'] = services.is_enable_for_voting(self.get_object())
        return context

    def get_queryset(self):
        return Article.objects.filter(date_deleted=None)


class ArticlesCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('articles.добавление_статьей', )
    template_name = 'articles/articles_create.html'
    model = Article
    context_object_name = 'article'
    form_class = ArticlesForm
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        # берем state из формы
        state_id = form.data['current_state'][0]
        state = State.objects.get(pk=state_id)
        form.instance.save()
        services.save_article(form.instance, state)
        return HttpResponseRedirect(redirect_to=reverse_lazy('articles'))


class ArticlesUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('articles.изменение_статьей',)
    template_name = 'articles/article_update.html'
    model = Article
    context_object_name = 'article'
    form_class = ArticlesForm

    def get_queryset(self):
        return Article.objects.filter(date_deleted=None)

    def form_valid(self, form):
        state_id = form.data['current_state'][0]
        state = State.objects.get(pk=state_id)
        form.instance.save()
        services.save_article(form.instance, state)
        return HttpResponseRedirect(redirect_to=self.object.get_detail_url())


@permission_required('articles.изменение_статьей')
def mark_as_republished(request, pk):
    article = Article.objects.get(pk=pk)
    services.republish_article(request.user, article)
    return HttpResponseRedirect(article.get_detail_url())


@permission_required('articles.изменение_статьей')
def remove_author_from_article(request, pk, author_id):
    article = Article.objects.get(pk=pk)
    author = Author.objects.get(pk=author_id)
    article.authors.remove(author)
    return HttpResponseRedirect(article.get_update_url())


@permission_required('articles.изменение_статьей')
def remove_user_from_article(request, pk, user_id):
    article = Article.objects.get(pk=pk)
    user = CustomUser.objects.get(pk=user_id)
    article.users.remove(user)
    return HttpResponseRedirect(article.get_update_url())


class SelectAuthorsList(PermissionRequiredMixin, ListView):
    permission_required = ('articles.изменение_статьей', )
    template_name = 'articles/add_author_to_article.html'
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
        article_pk = self.kwargs['pk']
        context['article'] = get_object_or_404(Article, pk=article_pk)
        context['filter'] = self.q_filter
        return context


class SelectUsersList(PermissionRequiredMixin, ListView):
    permission_required = ('articles.изменение_статьей',)
    template_name = 'articles/add_user_to_article.html'
    model = CustomUser
    context_object_name = 'users'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return CustomUser.objects.filter(date_deleted=None)

    def paginate_queryset(self, queryset, page_size):
        self.q_filter = CustomUserFilter(self.request.GET, queryset=self.get_queryset())
        return super().paginate_queryset(self.q_filter.qs, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = self.kwargs['pk']
        context['article'] = get_object_or_404(Article, pk=article_pk)
        context['filter'] = self.q_filter
        return context


@permission_required('articles.изменение_статьей')
def add_author_to_article(request, pk, author_id):
    article = Article.objects.get(pk=pk)
    author = Author.objects.get(pk=author_id)
    article.authors.add(author)
    return HttpResponseRedirect(article.get_update_url())


@permission_required('articles.изменение_статьей')
def add_user_to_article(request, pk, user_id):
    article = Article.objects.get(pk=pk)
    user = CustomUser.objects.get(pk=user_id)
    article.users.add(user)
    # отправляем уведомление о добавление в список ревьюверов
    create_reviewer_notification(request.user, article)
    return HttpResponseRedirect(article.get_update_url())


def download_article(request, pk):
    # скачивание файла
    article = Article.objects.get(pk=pk)
    filename = article.file.path
    response = FileResponse(open(filename, 'rb'))
    return response


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('articles.удаление_статьей', )
    model = Article
    success_url = reverse_lazy('articles')

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        services.delete_article(article)
        return HttpResponseRedirect(reverse_lazy('articles'))
