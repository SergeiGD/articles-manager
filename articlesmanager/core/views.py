from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import LoginForm


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('articles')

    def get_success_url(self):
        return reverse_lazy('articles')
