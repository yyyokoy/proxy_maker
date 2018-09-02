from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login

from django.views.generic import TemplateView
from django.views.generic import CreateView

from django.http import HttpResponseBadRequest
from django.shortcuts import redirect


class IndexView(TemplateView):
    template_name = "accounts/index.html"

class Login(LoginView):
    """ログインページ"""
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'main/index.html'

class UserCreate(CreateView):
    """ユーザー登録"""
    template_name = 'accounts/user_create.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        """正しければ登録"""
        try:
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(self.request, user)

            return redirect('main:index')

        except:
            return HttpResponseBadRequest()
