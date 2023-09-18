from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=150,
                               help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Please Enter Your Username'}))

    # help_text imported from source password1 in class Meta
    password1 = forms.CharField(label='Password', max_length=100,
                                help_text=password_validation.password_validators_help_text_html(),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Please Enter Your Password'}))
    password2 = forms.CharField(label='Confirm Password', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Please Enter Your Confirm Password'}))

    email = forms.EmailField(label='Email', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Email Address (It is not required)'}))
    first_name = forms.CharField(label='First Name', required=False, max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'First Name (It is not required)'}))
    last_name = forms.CharField(label='Last Name', required=False, max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Last Name (It is not required)'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']


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


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'profile_bio', 'facebook_link', 'instagram_link', 'linkedin_link']

    profile_image = forms.ImageField(required=False)
    profile_bio = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'placeholder': 'Please Enter Your Bio'}))
    facebook_link = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Please Enter Your Facebook Link'}))
    instagram_link = forms.CharField(required=False,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Please Enter Your Instagram Link'}))
    linkedin_link = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Please Enter Your Instagram Link'}))


class UpdateUserForm(UserChangeForm):
    username = forms.CharField(label='Username', max_length=150,
                               help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Please Enter Your Username'}))

    email = forms.EmailField(label='Email', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Email Address (It is not required)'}))
    first_name = forms.CharField(label='First Name', required=False, max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'First Name (It is not required)'}))
    last_name = forms.CharField(label='Last Name', required=False, max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Last Name (It is not required)'}))

    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name']
