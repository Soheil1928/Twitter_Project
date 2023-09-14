from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'accounts/register_page.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password1')
            user = authenticate(request,username=username, password=password)
            if user is None:
                register_form.save()
                messages.success(request, 'You Have Successfully Register.', 'success')
                return redirect('login')
            else:
                messages.error(request, 'Username or Password Is Invalid...', 'danger')
                return render(request, 'accounts/register_page.html', {'register_form': register_form})

        messages.error(request, 'Username or Password Is Invalid...', 'danger')
        return render(request, 'accounts/register_page.html', {'register_form': register_form})


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login_page.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have Been Logged In...!', 'success')
            return redirect('home_page')
        else:
            messages.error(request, 'Username or Password Is Invalid...', 'danger')
            return render(request, 'accounts/login_page.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You Have Been Logged Out...!', 'success')
        return redirect('home_page')
