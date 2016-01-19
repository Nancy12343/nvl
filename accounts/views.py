from django.utils import timezone
from django.views.generic.edit import FormView, View
from django.views.generic.base import TemplateView
from .forms import AccountForm, RegisterForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .models import Account
from django.shortcuts import redirect, render, HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.auth.models import User

class LoginView(FormView):
    form_class = AccountForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:login')

    # def get_initial(self):
    #     return {'username': self.request.GET.get('username', '')}

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            account = Account.objects.filter(user=user)
            if account.exists():
                return redirect('novels:home')
                # return HttpResponseRedirect('accounts/home.html')
            else:
            #     url = '%s?error_message=Invalid Username and / or Password&username=%s' %(url, username)
                url = self.template_name
                return redirect(url)
        else:
            return self.form_invalid(form)


class RegistView(FormView):
    form_class = RegisterForm
    template_name = 'accounts/regist.html'
    success_url = reverse_lazy('accounts:regist')

    def form_valid(self, form):
        nickname = form.cleaned_data.get('nickname')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        accounts = Account.objects.all()
        for account in accounts:
            if account.email == email:
                url = '%s?error_message=The Email already registed' %self.success_url
                return redirect(url)
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            if user:
                acc = Account()
                acc.email = email
                acc.user = user
                acc.role = Account.READER
                acc.name = nickname
                acc.save()
                user = authenticate(username=username, password=password)
                login(self.request, user)
                return redirect('novels:home')
        except Exception, e:
            return self.form_invalid(form)

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('accounts:login')


