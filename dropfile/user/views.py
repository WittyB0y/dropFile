from django.contrib.auth import login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from user.forms import RegisterUserForm, LoginUserForm


class ProfileForm:
    pass


class RegisterUser(UserPassesTestMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'user/signup.html'
    second_form_class = ProfileForm
    permission_denied_message = ("You are already registered!")

    def test_func(self):
        return self.request.user.is_anonymous

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Авторизация")
    #     return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')
