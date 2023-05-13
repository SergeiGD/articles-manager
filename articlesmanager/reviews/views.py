from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from .models import Review
from articles.models import Article
from .forms import ReviewsForm


class ReviewsList(LoginRequiredMixin, ListView):
    template_name = 'reviews/reviews_list.html'
    model = Article
    context_object_name = 'articles'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return self.request.user.get_articles_to_review()


class ReviewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('add_review',)
    template_name = 'reviews/review_create.html'
    model = Review
    context_object_name = 'review'
    form_class = ReviewsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        context['article'] = article
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        article = context['article']
        if self.request.user not in article.users.all():
            raise PermissionDenied('Вы не являетесь рецензентом этой статьи')
        form.instance.article = article
        form.instance.user = self.request.user
        form.instance.save()
        return HttpResponseRedirect(redirect_to=form.instance.article.get_show_url())


class ReviewDetail(LoginRequiredMixin, DetailView):
    template_name = 'reviews/review_detail.html'
    model = Review
    context_object_name = 'review'
    pk_url_kwarg = 'review_id'
