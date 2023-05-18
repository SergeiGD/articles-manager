from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from .models import UserGroup, GroupPermission
from .forms import GroupsForm
from users.models import CustomUser
from .filters import GroupFilter, PermissionFilter
from users.filters import CustomUserFilter


class GroupsList(LoginRequiredMixin, ListView):
    template_name = 'groups/groups_list.html'
    model = UserGroup
    context_object_name = 'groups'
    paginator_class = Paginator
    paginate_by = 8

    def paginate_queryset(self, queryset, page_size):
        self.q_filter = GroupFilter(self.request.GET, queryset=self.get_queryset())
        return super().paginate_queryset(self.q_filter.qs, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.q_filter
        return context


class GroupsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('groups.добавление_групп',)
    template_name = 'groups/groups_create.html'
    model = UserGroup
    context_object_name = 'group'
    form_class = GroupsForm
    success_url = reverse_lazy('groups')


class GroupsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('groups.изменение_групп',)
    template_name = 'groups/groups_update.html'
    model = UserGroup
    context_object_name = 'group'
    form_class = GroupsForm

    def get_success_url(self):
        return self.object.get_detail_url()


class GroupsDetail(LoginRequiredMixin, DetailView):
    template_name = 'groups/groups_detai.html'
    model = UserGroup
    context_object_name = 'group'


class GroupsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('groups.удаление_групп',)
    model = UserGroup
    success_url = reverse_lazy('groups')


class SelectPermissionsList(PermissionRequiredMixin, ListView):
    permission_required = ('groups.изменение_групп',)
    template_name = 'groups/add_permission_to_group.html'
    model = GroupPermission
    context_object_name = 'permissions'
    paginator_class = Paginator
    paginate_by = 8

    def paginate_queryset(self, queryset, page_size):
        self.q_filter = PermissionFilter(self.request.GET, queryset=self.get_queryset())
        return super().paginate_queryset(self.q_filter.qs, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_pk = self.kwargs['pk']
        context['group'] = get_object_or_404(UserGroup, pk=group_pk)
        context['filter'] = self.q_filter
        return context


@permission_required('groups.изменение_групп')
def add_permission_to_group(request, pk, permission_id):
    group = UserGroup.objects.get(pk=pk)
    permission = GroupPermission.objects.get(pk=permission_id)
    group.permissions.add(permission)
    return HttpResponseRedirect(group.get_update_url())


@permission_required('groups.изменение_групп')
def remove_permission_from_group(request, pk, permission_id):
    group = UserGroup.objects.get(pk=pk)
    permission = GroupPermission.objects.get(pk=permission_id)
    group.permissions.remove(permission)
    return HttpResponseRedirect(group.get_update_url())



class SelectUsersList(PermissionRequiredMixin, ListView):
    permission_required = ('groups.изменение_групп', 'users.изменение_пользователей')
    template_name = 'groups/add_users_to_group.html'
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
        group_pk = self.kwargs['pk']
        context['group'] = get_object_or_404(UserGroup, pk=group_pk)
        context['filter'] = self.q_filter
        return context


@permission_required('groups.изменение_групп', 'users.изменение_пользователей')
def add_user_to_group(request, pk, user_id):
    group = UserGroup.objects.get(pk=pk)
    user = CustomUser.objects.get(pk=user_id)
    group.user_set.add(user)
    return HttpResponseRedirect(group.get_update_url())


@permission_required('groups.изменение_групп', 'users.изменение_пользователей')
def remove_user_from_group(request, pk, user_id):
    group = UserGroup.objects.get(pk=pk)
    user = CustomUser.objects.get(pk=user_id)
    group.user_set.remove(user)
    return HttpResponseRedirect(group.get_update_url())
