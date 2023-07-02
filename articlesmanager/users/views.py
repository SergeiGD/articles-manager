from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from .models import CustomUser, Position
from .forms import CreateUsersForm, PositionForm, UpdateUserForm, ResetPasswordForm
from groups.models import UserGroup
from .filters import CustomUserFilter, PositionFilter
from groups.filters import GroupFilter
from . import services


class UsersList(LoginRequiredMixin, ListView):
    template_name = 'users/users_list.html'
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
        context['filter'] = self.q_filter
        return context


class UsersCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('users.добавление_пользователей', )
    template_name = 'users/users_create.html'
    model = CustomUser
    context_object_name = 'user'
    form_class = CreateUsersForm
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        self.object = form.save()
        password = services.register_user(self.object)
        return render(self.request, 'users/password_set_info.html', context={'user': self.object, 'password': password})
        #return HttpResponseRedirect(self.get_success_url(), kwargs={'user': self.object, 'password': password})


class UsersDetail(LoginRequiredMixin, DetailView):
    template_name = 'users/users_detail.html'
    model = CustomUser
    context_object_name = 'user'

    def get_queryset(self):
        return CustomUser.objects.filter(date_deleted=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_link'] = self.get_object().get_delete_url()
        return context


class UsersUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('users.изменение_пользователей', )
    template_name = 'users/users_update.html'
    model = CustomUser
    context_object_name = 'user'
    form_class = UpdateUserForm

    def get_success_url(self):
        return self.object.get_detail_url()

    def get_queryset(self):
        return CustomUser.objects.filter(date_deleted=None)


class UsersDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('users.удаление_пользователей',)
    model = CustomUser
    success_url = reverse_lazy('users')

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        services.delete_user(user)
        return HttpResponseRedirect(reverse_lazy('users'))


@permission_required('users.изменение_пользователей')
def reset_user_password(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    password = services.reset_user(user)
    return render(request, 'users/password_set_info.html', context={'user': user, 'password': password})


class PositionsList(LoginRequiredMixin, ListView):
    template_name = 'users/positions_list.html'
    model = Position
    context_object_name = 'positions'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return Position.objects.filter(date_deleted=None)

    def paginate_queryset(self, queryset, page_size):
        self.q_filter = PositionFilter(self.request.GET, queryset=self.get_queryset())
        return super().paginate_queryset(self.q_filter.qs, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.q_filter
        return context


class PositionsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('users.добавление_должностей',)
    template_name = 'users/positions_create.html'
    model = Position
    context_object_name = 'positions'
    form_class = PositionForm
    success_url = reverse_lazy('positions')


class PositionsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('users.изменение_должностей',)
    template_name = 'users/positions_update.html'
    model = Position
    context_object_name = 'position'
    form_class = PositionForm

    def get_success_url(self):
        return self.object.get_detail_url()

    def get_queryset(self):
        return Position.objects.filter(date_deleted=None)


class PositionsDetail(LoginRequiredMixin, DetailView):
    template_name = 'users/positions_detail.html'
    model = Position
    context_object_name = 'position'

    def get_queryset(self):
        return Position.objects.filter(date_deleted=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_link'] = self.get_object().get_delete_url()
        return context


class PositionsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('users.удаление_должностей',)
    model = Position
    success_url = reverse_lazy('positions')


    def post(self, request, *args, **kwargs):
        position = self.get_object()
        services.delete_position(position)
        return HttpResponseRedirect(reverse_lazy('positions'))


class SelectGroupsList(PermissionRequiredMixin, ListView):
    """
    Вью для добавления группы юзеру
    """
    permission_required = ('users.изменение_пользователей', )
    template_name = 'users/add_group_to_user.html'
    model = UserGroup
    context_object_name = 'groups'
    paginator_class = Paginator
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.kwargs['pk']
        context['user'] = get_object_or_404(CustomUser, pk=user_pk)
        context['filter'] = self.q_filter
        return context

    def paginate_queryset(self, queryset, page_size):
        self.q_filter = GroupFilter(self.request.GET, queryset=self.get_queryset())
        return super().paginate_queryset(self.q_filter.qs, page_size)


@permission_required('users.изменение_пользователей')
def add_group_to_user(request, pk, group_id):
    group = UserGroup.objects.get(pk=group_id)
    user = CustomUser.objects.get(pk=pk)
    group.user_set.add(user)
    return HttpResponseRedirect(user.get_update_url())


@permission_required('users.изменение_пользователей')
def remove_group_from_user(request, pk, group_id):
    group = UserGroup.objects.get(pk=group_id)
    user = CustomUser.objects.get(pk=pk)
    group.user_set.remove(user)
    return HttpResponseRedirect(user.get_update_url())
