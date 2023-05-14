from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from .models import Notification

class NotificationsList(LoginRequiredMixin, ListView):
    template_name = 'notifications/notifications_list.html'
    model = Notification
    context_object_name = 'notifications'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return Notification.objects.all(user=self.request.user)
