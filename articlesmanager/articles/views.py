from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.core.paginator import Paginator
from .models import Article, ArticleState
from authors.models import Author
from states.models import State
from .forms import ArticlesForm
import json

class ArticlesList(ListView):
    template_name = 'articles/articles_list.html'
    model = Article
    context_object_name = 'articles'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return Article.objects.filter(date_deleted=None)


class ArticlesDetail(DetailView):
    template_name = 'articles/articles_detail.html'
    model = Article
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.filter(date_deleted=None)


class ArticlesCreate(CreateView):
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


class ArticlesUpdate(UpdateView):
    template_name = 'articles/article_update.html'
    model = Article
    context_object_name = 'article'
    form_class = ArticlesForm
    success_url = reverse_lazy('articles')

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
        return HttpResponseRedirect(redirect_to=reverse_lazy('articles'))


def remove_author_from_article(request, pk, author_id):
    article = Article.objects.get(pk=pk)
    author = Author.objects.get(pk=author_id)
    article.authors.remove(author)
    return HttpResponseRedirect(article.get_update_url())


def select_author(request, pk):
    article = Article.objects.get(pk=pk)
    context = {'article': article, 'authors': Author.objects.filter(date_deleted=None)}
    return render(request, 'articles/add_author_to_article.html', context)


def add_author_to_article(request, pk, author_id):
    article = Article.objects.get(pk=pk)
    author = Author.objects.get(pk=author_id)
    article.authors.add(author)
    return HttpResponseRedirect(article.get_update_url())


def download_article(request, pk):
    article = Article.objects.get(pk=pk)
    filename = article.file.path
    response = FileResponse(open(filename, 'rb'))
    return response


class ArticlesDelete(DeleteView):
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
