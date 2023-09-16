from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='', max_length=150,
                               help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'User Name'}))

    # help_text imported from source password1 in class Meta
    password1 = forms.CharField(label='', max_length=100,
                                help_text=password_validation.password_validators_help_text_html(),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Password'}))
    password2 = forms.CharField(label='', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ChangePasswordForm(forms.Form):
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Please Enter Username'}))
    old_password = forms.CharField(label='Old Password', max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Please Enter Old Password'}))
    new_password = forms.CharField(label='New Password', max_length=100,
                                   help_text=password_validation.password_validators_help_text_html(),
                                   widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Please Enter New Password'}))
    confirm_new_password = forms.CharField(label='Confirm New Password', max_length=100,
                                           widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                             'placeholder': 'Please Repeat Username'}))
