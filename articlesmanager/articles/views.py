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
from notifications.models import Notification
from notifications.utils import create_reviewer_notification, create_republished_notification
import json

class ArticlesList(LoginRequiredMixin, ListView):
    template_name = 'articles/articles_list.html'
    model = Article
    context_object_name = 'articles'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return Article.objects.filter(date_deleted=None)


class ArticlesDetail(LoginRequiredMixin, DetailView):
    template_name = 'articles/articles_detail.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_create_review'] = self.request.user.can_create_review(self.object)
        return context

    def get_queryset(self):
        return Article.objects.filter(date_deleted=None)


class ArticlesCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('add_article', )
    template_name = 'articles/articles_create.html'
    model = Article
    context_object_name = 'article'
    form_class = ArticlesForm
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        state_id = form.data['current_state'][0]
        state = State.objects.get(pk=state_id)
        form.instance.save()
        form.instance.states.add(state)
        return HttpResponseRedirect(redirect_to=reverse_lazy('articles'))

    def form_invalid(self, form):
        response = HttpResponse(json.dumps({'errors': form.errors}), status=400, content_type='application/json')
        return response


class ArticlesUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('change_article',)
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
        if form.instance.get_current_state() != state:
            ArticleState.objects.update_or_create(
                state_id=state_id,
                article_id=form.instance.pk,
                date_set=timezone.now()
            )
        return HttpResponseRedirect(redirect_to=self.object.get_show_url())


@permission_required('change_article')
def mark_as_republished(request, pk):
    article = Article.objects.get(pk=pk)
    article.date_repulished = timezone.now()
    article.save()
    Notification.objects.create(
        user=user,
        subject=Notification.NotificationsSubjects.ARTICLE_REPUBLISHED,
        content=create_republished_notification(article),
    )
    return HttpResponseRedirect(article.get_show_url())


@permission_required('change_article')
def remove_author_from_article(request, pk, author_id):
    article = Article.objects.get(pk=pk)
    author = Author.objects.get(pk=author_id)
    article.authors.remove(author)
    return HttpResponseRedirect(article.get_update_url())


@permission_required('change_article')
def remove_user_from_article(request, pk, user_id):
    article = Article.objects.get(pk=pk)
    user = CustomUser.objects.get(pk=user_id)
    article.users.remove(user)
    return HttpResponseRedirect(article.get_update_url())


class SelectAuthorsList(PermissionRequiredMixin, ListView):
    permission_required = ('change_article', )
    template_name = 'articles/add_author_to_article.html'
    model = Author
    context_object_name = 'authors'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return Author.objects.filter(date_deleted=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = self.kwargs['pk']
        context['article'] = get_object_or_404(Article, pk=article_pk)
        return context


class SelectUsersList(PermissionRequiredMixin, ListView):
    permission_required = ('change_article',)
    template_name = 'articles/add_user_to_article.html'
    model = CustomUser
    context_object_name = 'users'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return CustomUser.objects.filter(date_deleted=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = self.kwargs['pk']
        context['article'] = get_object_or_404(Article, pk=article_pk)
        return context


@permission_required('change_article')
def add_author_to_article(request, pk, author_id):
    article = Article.objects.get(pk=pk)
    author = Author.objects.get(pk=author_id)
    article.authors.add(author)
    return HttpResponseRedirect(article.get_update_url())


@permission_required('change_article')
def add_user_to_article(request, pk, user_id):
    article = Article.objects.get(pk=pk)
    user = CustomUser.objects.get(pk=user_id)
    article.users.add(user)
    Notification.objects.create(
        user=user,
        subject=Notification.NotificationsSubjects.REVIEWER,
        content=create_reviewer_notification(article),
    )
    return HttpResponseRedirect(article.get_update_url())


def download_article(request, pk):
    article = Article.objects.get(pk=pk)
    filename = article.file.path
    response = FileResponse(open(filename, 'rb'))
    return response


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('delete_article', )
    model = Article
    success_url = reverse_lazy('articles')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        article = self.get_object()
        article.date_deleted = timezone.now()
        article.save()
        return HttpResponseRedirect(self.get_success_url())
