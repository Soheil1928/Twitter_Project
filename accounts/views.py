from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, ChangePasswordForm, UpdateProfileForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'accounts/register_page.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
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


class ChangePasswordView(View):
    def get(self, request):
        change_password_form = ChangePasswordForm()
        return render(request, 'accounts/change_password.html', {'change_password_form': change_password_form})

    def post(self, request):
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            user = User.objects.filter(username__exact=change_password_form.cleaned_data.get('username')).first()
            if user is not None:
                old_pass = change_password_form.cleaned_data.get('old_password')
                correct_password = user.check_password(old_pass)
                if correct_password:
                    new_pass = change_password_form.cleaned_data.get('new_password')
                    confirm_new_pass = change_password_form.cleaned_data.get('confirm_new_password')
                    if new_pass == confirm_new_pass:
                        user.set_password(new_pass)
                        user.save()
                        messages.success(request, 'Change Password Successfully... ', 'success')
                        return redirect('login')
                    else:
                        messages.error(request, 'Password Is Invalid...', 'danger')
                        return render(request, 'accounts/change_password.html',
                                      {'change_password_form': change_password_form})
                else:
                    messages.error(request, 'Password Is Invalid...', 'danger')
                    return render(request, 'accounts/change_password.html',
                                  {'change_password_form': change_password_form})
            else:
                messages.error(request, 'Username or Password Is Invalid...', 'danger')
                return render(request, 'accounts/change_password.html', {'change_password_form': change_password_form})

        messages.error(request, 'Username or Password Is Invalid...', 'danger')
        return render(request, 'accounts/change_password.html', {'change_password_form': change_password_form})


class UpdateProfile(View):
    def get(self, request):
        if request.user.is_authenticated:
            usr = User.objects.get(id=request.user.id)
            user_form = UpdateUserForm(instance=usr)
            prof = Profile.objects.get(id=request.user.id)
            profile_form = UpdateProfileForm(instance=prof)
            return render(request, 'accounts/update_profile_page.html', {'user_form': user_form,
                                                                         'profile_form': profile_form})
        else:
            messages.error(request, 'Please Login To Continue...!', 'danger')
            return redirect('home_page')

    def post(self, request):
        if request.user.is_authenticated:
            usr = User.objects.get(id=request.user.id)
            user_form = UpdateUserForm(request.POST, instance=usr)
            prof = Profile.objects.get(id=request.user.id)
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=prof)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('home_page')
            else:
                return render(request, 'accounts/update_profile_page.html', {'user_form': user_form,
                                                                             'profile_form': profile_form})
        else:
            messages.error(request, 'Please Login To Continue...!', 'danger')
            return redirect('login')
