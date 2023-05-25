from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator

from notifications.models import Notification
from .models import Voting, VotingUsers
from articles.models import Article
from .forms import VotingForm
from notifications.services import create_voting_notification
from .filters import VotingFilter
from .services import change_vote, get_current_vote, is_enable_to_vote, create_vote


class VotingsList(LoginRequiredMixin, ListView):
    template_name = 'votings/votings_list.html'
    model = Voting
    context_object_name = 'votings'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return Voting.objects.filter(article__date_deleted=None)

    def paginate_queryset(self, queryset, page_size):
        self.q_filter = VotingFilter(self.request.GET, queryset=self.get_queryset())
        return super().paginate_queryset(self.q_filter.qs, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.q_filter
        return context


class VotingsCreate(LoginRequiredMixin, CreateView):
    template_name = 'votings/votings_create.html'
    model = Voting
    context_object_name = 'voting'
    form_class = VotingForm
    success_url = reverse_lazy('votings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        context['article'] = article
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        article = context['article']
        if article.votings.exists():
            return HttpResponseRedirect(redirect_to=article.votings.first().get_detail_url())
        form.instance.article = article
        form.instance.save()
        create_voting_notification(form.instance, article)
        return HttpResponseRedirect(redirect_to=form.instance.get_detail_url())


class VotingsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ['change_voting', ]
    template_name = 'votings/votings_update.html'
    model = Voting
    context_object_name = 'voting'
    form_class = VotingForm

    def get_success_url(self):
        return self.object.get_detail_url()


class VotingsDetail(DetailView):
    template_name = 'votings/votings_details.html'
    model = Voting
    context_object_name = 'voting'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_vote = self.request.user.votingusers_set.filter(voting_id=self.object.id).first()
        # определяем текущий голос
        context['current_vote'] = get_current_vote(user_vote)
        # определяем, началось ли уже голосование
        enable_to_vote = is_enable_to_vote(self.object)
        context['enable_to_vote'] = enable_to_vote
        return context


def voting_agreed(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    user_voting = VotingUsers.objects.filter(
        voting_id=voting.id,
        user_id=request.user.id,
    ).first()
    if user_voting is not None:
        # если уже юзер уже голосовал и изменил голос
        change_vote(user_voting, True)
    else:
        create_vote(voting, request.user, True)
    return HttpResponseRedirect(redirect_to=voting.get_detail_url())


def voting_disagreed(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    user_voting = VotingUsers.objects.filter(
        voting_id=voting.id,
        user_id=request.user.id,
    ).first()
    if user_voting is not None:
        # если уже юзер уже голосовал и изменил голос
        change_vote(user_voting, False)
    else:
        create_vote(voting, request.user, False)
    return HttpResponseRedirect(redirect_to=voting.get_detail_url())
