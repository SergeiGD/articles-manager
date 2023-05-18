from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from .models import Notification
from .filters import NotificationFilter

class NotificationsList(LoginRequiredMixin, ListView):
    template_name = 'notifications/notifications_list.html'
    model = Notification
    context_object_name = 'notifications'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def paginate_queryset(self, queryset, page_size):
        self.q_filter = NotificationFilter(self.request.GET, queryset=self.get_queryset())
        return super().paginate_queryset(self.q_filter.qs, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.q_filter
        return context


class NotificationsDetail(LoginRequiredMixin, DetailView):
    template_name = 'notifications/notifications_detail.html'
    model = Notification
    context_object_name = 'notification'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_link'] = self.get_object().get_delete_url()
        return context


def mark_as_checked(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.checked = True
    notification.save()
    return HttpResponseRedirect(notification.get_detail_url())


class NotificationsDelete(LoginRequiredMixin, DeleteView):
    model = Notification
    success_url = reverse_lazy('notifications')
