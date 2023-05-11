from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from .models import CustomUser
from .forms import CreateUsersForm

class UsersList(ListView):
    template_name = 'users/users_list.html'
    model = CustomUser
    context_object_name = 'users'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return CustomUser.objects.filter(date_deleted=None)


class UsersCreate(CreateView):
    template_name = 'users/users_create.html'
    model = CustomUser
    context_object_name = 'user'
    form_class = CreateUsersForm
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        self.object: CustomUser = form.save()
        password = form.cleaned_data['password']
        self.object.set_password(password)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
