from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from .models import State
from .forms import StatesForm
from .filters import StateFilter


class StatesList(LoginRequiredMixin, ListView):
    template_name = 'states/states_list.html'
    model = State
    context_object_name = 'states'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return State.objects.filter(date_deleted=None)

    def paginate_queryset(self, queryset, page_size):
        self.q_filter = StateFilter(self.request.GET, queryset=self.get_queryset())
        return super().paginate_queryset(self.q_filter.qs, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.q_filter
        return context


class StatesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('states.добавление_статусов',)
    template_name = 'states/states_create.html'
    model = State
    context_object_name = 'states'
    form_class = StatesForm
    success_url = reverse_lazy('states')


class StatesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('states.изменение_статусов',)
    template_name = 'states/states_update.html'
    model = State
    context_object_name = 'state'
    form_class = StatesForm

    def get_success_url(self):
        return self.object.get_detail_url()

    def get_queryset(self):
        return State.objects.filter(date_deleted=None)


class StatesDetail(LoginRequiredMixin, DetailView):
    template_name = 'states/states_detail.html'
    model = State
    context_object_name = 'state'

    def get_queryset(self):
        return State.objects.filter(date_deleted=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_link'] = self.get_object().get_delete_url()
        return context


class StatesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('states.удаление_статусов', )
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
