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


class GroupsList(PermissionRequiredMixin, ListView):
    permission_required = ('view_usergroup', )
    template_name = 'groups/groups_list.html'
    model = UserGroup
    context_object_name = 'groups'
    paginator_class = Paginator
    paginate_by = 8


class GroupsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('add_usergroup',)
    template_name = 'groups/groups_create.html'
    model = UserGroup
    context_object_name = 'group'
    form_class = GroupsForm
    success_url = reverse_lazy('groups')


class GroupsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('change_usergroup',)
    template_name = 'groups/groups_update.html'
    model = UserGroup
    context_object_name = 'group'
    form_class = GroupsForm
    success_url = reverse_lazy('groups')


class GroupsDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('view_usergroup',)
    template_name = 'groups/groups_detai.html'
    model = UserGroup
    context_object_name = 'group'


class GroupsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('delete_usergroup',)
    model = UserGroup
    success_url = reverse_lazy('groups')


class SelectPermissionsList(PermissionRequiredMixin, ListView):
    permission_required = ('view_usergroup',)
    template_name = 'groups/add_permission_to_group.html'
    model = GroupPermission
    context_object_name = 'permissions'
    paginator_class = Paginator
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_pk = self.kwargs['pk']
        context['group'] = get_object_or_404(UserGroup, pk=group_pk)
        return context


@permission_required('change_usergroup')
def add_permission_to_group(request, pk, permission_id):
    group = UserGroup.objects.get(pk=pk)
    permission = GroupPermission.objects.get(pk=permission_id)
    group.permissions.add(permission)
    return HttpResponseRedirect(group.get_update_url())


@permission_required('change_usergroup')
def remove_permission_from_group(request, pk, permission_id):
    group = UserGroup.objects.get(pk=pk)
    permission = GroupPermission.objects.get(pk=permission_id)
    group.permissions.remove(permission)
    return HttpResponseRedirect(group.get_update_url())



class SelectUsersList(PermissionRequiredMixin, ListView):
    permission_required = ('change_usergroup',)
    template_name = 'groups/add_users_to_group.html'
    model = CustomUser
    context_object_name = 'users'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return CustomUser.objects.filter(date_deleted=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_pk = self.kwargs['pk']
        context['group'] = get_object_or_404(UserGroup, pk=group_pk)
        return context


@permission_required('change_usergroup')
def add_user_to_group(request, pk, user_id):
    group = UserGroup.objects.get(pk=pk)
    user = CustomUser.objects.get(pk=user_id)
    group.user_set.add(user)
    return HttpResponseRedirect(group.get_update_url())


@permission_required('change_usergroup')
def remove_user_from_group(request, pk, user_id):
    group = UserGroup.objects.get(pk=pk)
    user = CustomUser.objects.get(pk=user_id)
    group.user_set.remove(user)
    return HttpResponseRedirect(group.get_update_url())
