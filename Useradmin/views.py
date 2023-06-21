from django.contrib.auth import (
    login as auth_login,
)
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from .forms import MySignUpForm
from .models import MyUser


class MySignUp(generic.CreateView):
    form_class = MySignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        """Security check complete. Log the user in. PERFORM CUSTOM CODE."""
        auth_login(self.request, form.get_user())
        form.get_user().execute_after_login()
        return HttpResponseRedirect(self.get_success_url())


class MyUserListView(generic.ListView):
    model = MyUser
    context_object_name = 'all_myusers'
    template_name = 'myuser_list.html'
