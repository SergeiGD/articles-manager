from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from .models import CustomUser, Position
from .forms import CreateUsersForm, PositionForm, UpdateUserForm, ResetPasswordForm

class UsersList(LoginRequiredMixin, ListView):
    template_name = 'users/users_list.html'
    model = CustomUser
    context_object_name = 'users'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return CustomUser.objects.filter(date_deleted=None)


class UsersCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('add_customuser', )
    template_name = 'users/users_create.html'
    model = CustomUser
    context_object_name = 'user'
    form_class = CreateUsersForm
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        self.object = form.save()
        password = form.data['password']
        email = EmailMessage(
            subject='Регистрация',
            body=f'Ваш аккаунт создан. Пароль - {password}',
            to=[self.object.email, ],
        )
        email.send()
        return HttpResponseRedirect(self.get_success_url())


class UsersDetail(LoginRequiredMixin, DetailView):
    template_name = 'users/users_detail.html'
    model = CustomUser
    context_object_name = 'user'

    def get_queryset(self):
        return CustomUser.objects.filter(date_deleted=None)


class UsersUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('change_customuser', )
    template_name = 'users/users_update.html'
    model = CustomUser
    context_object_name = 'user'
    form_class = UpdateUserForm

    def get_success_url(self):
        return self.object.get_detail_url()

    def get_queryset(self):
        return CustomUser.objects.filter(date_deleted=None)


class UsersDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('delete_customuser',)
    model = CustomUser
    success_url = reverse_lazy('users')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.date_deleted = timezone.now()
        user.save()
        return HttpResponseRedirect(self.get_success_url())


@permission_required('change_customuser')
def reset_user_password(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'GET':
        form = ResetPasswordForm()
        return render(request, 'users/reset_password.html', {'form': form, 'user': user})
    else:
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.data['password']
            user.set_password(password)
            user.save()
            email = EmailMessage(
                subject='Изменение пароля',
                body=f'Ваш пароль был изменен на {password}',
                to=[user.email, ],
            )
            email.send()
            return HttpResponseRedirect(user.get_detail_url())

        return render(request, 'users/reset_password.html', {'form': form, 'user': user})


class PositionsList(LoginRequiredMixin, ListView):
    template_name = 'users/positions_list.html'
    model = Position
    context_object_name = 'positions'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return Position.objects.filter(date_deleted=None)


class PositionsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('add_position',)
    template_name = 'users/positions_create.html'
    model = Position
    context_object_name = 'positions'
    form_class = PositionForm
    success_url = reverse_lazy('positions')


class PositionsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('change_position',)
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


class PositionsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('delete_position',)
    model = Position
    success_url = reverse_lazy('positions')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        position = self.get_object()
        position.date_deleted = timezone.now()
        position.save()
        return HttpResponseRedirect(self.get_success_url())
