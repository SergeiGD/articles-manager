from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator
from .models import Review
from articles.models import Article


class ReviewsList(LoginRequiredMixin, ListView):
    template_name = 'reviews/reviews_list.html'
    model = Article
    context_object_name = 'articles'
    paginator_class = Paginator
    paginate_by = 8

    def get_queryset(self):
        a = self.request.user.get_articles_to_review()
        print(a)
        return a


# class StatesCreate(CreateView):
#     template_name = 'states/states_create.html'
#     model = Review
#     context_object_name = 'review'
#     form_class = StatesForm
#     success_url = reverse_lazy('states')
#
#
# class StatesUpdate(UpdateView):
#     template_name = 'states/states_update.html'
#     model = State
#     context_object_name = 'state'
#     form_class = StatesForm
#     success_url = reverse_lazy('states')
#
#     def get_queryset(self):
#         return State.objects.filter(date_deleted=None)
#
#
# class StatesDetail(DeleteView):
#     template_name = 'states/states_detail.html'
#     model = State
#     context_object_name = 'state'
#
#     def get_queryset(self):
#         return State.objects.filter(date_deleted=None)
#
#
# class StatesDelete(DeleteView):
#     model = State
#     success_url = reverse_lazy('states')
#
#     def delete(self, request, *args, **kwargs):
#         """
#         Call the delete() method on the fetched object and then redirect to the
#         success URL.
#         """
#         state = self.get_object()
#         state.date_deleted = timezone.now()
#         state.save()
#         return HttpResponseRedirect(self.get_success_url())
