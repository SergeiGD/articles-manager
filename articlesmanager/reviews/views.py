from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from .models import Review
from articles.models import Article
from .forms import ReviewsForm
from .filters import ArticlesToReviewFilter
from . import services
from users.services import get_articles_to_review


class ReviewsList(LoginRequiredMixin, ListView):
    template_name = 'reviews/reviews_list.html'
    model = Article
    context_object_name = 'articles'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return get_articles_to_review(self.request.user)

    def paginate_queryset(self, queryset, page_size):
        self.q_filter = ArticlesToReviewFilter(self.request.GET, queryset=self.get_queryset())
        return super().paginate_queryset(self.q_filter.qs, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.q_filter
        return context


class ReviewsCreate(LoginRequiredMixin, CreateView):
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
        services.create_review(form.instance, self.request.user, article)
        return HttpResponseRedirect(redirect_to=form.instance.article.get_detail_url())


class ReviewDetail(LoginRequiredMixin, DetailView):
    template_name = 'reviews/review_detail.html'
    model = Review
    context_object_name = 'review'
    pk_url_kwarg = 'review_id'


class ReviewUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'reviews/review_update.html'
    model = Review
    context_object_name = 'review'
    form_class = ReviewsForm

    def get_success_url(self):
        return self.get_object().article.get_detail_url()

    def form_valid(self, form):
        services.check_is_reviewer(self.request.user, self.get_object().article)
        form.instance.save()
        return HttpResponseRedirect(redirect_to=form.instance.article.get_detail_url())
