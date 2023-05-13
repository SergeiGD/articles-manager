from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from .models import State
from .forms import StatesForm

class StatesList(LoginRequiredMixin, ListView):
    template_name = 'states/states_list.html'
    model = State
    context_object_name = 'states'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return State.objects.filter(date_deleted=None)


class StatesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('add_state',)
    template_name = 'states/states_create.html'
    model = State
    context_object_name = 'states'
    form_class = StatesForm
    success_url = reverse_lazy('states')


class StatesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('change_state',)
    template_name = 'states/states_update.html'
    model = State
    context_object_name = 'state'
    form_class = StatesForm
    success_url = reverse_lazy('states')

    def get_queryset(self):
        return State.objects.filter(date_deleted=None)


class StatesDetail(LoginRequiredMixin, DetailView):
    template_name = 'states/states_detail.html'
    model = State
    context_object_name = 'state'

    def get_queryset(self):
        return State.objects.filter(date_deleted=None)


class StatesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('delete_state', )
    model = State
    success_url = reverse_lazy('states')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        state = self.get_object()
        state.date_deleted = timezone.now()
        state.save()
        return HttpResponseRedirect(self.get_success_url())
