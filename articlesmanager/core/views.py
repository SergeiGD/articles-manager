from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import LoginForm


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('notifications')

    def get_success_url(self):
        return reverse_lazy('notifications')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    return redirect('login')
