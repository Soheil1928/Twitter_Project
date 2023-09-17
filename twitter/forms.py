from django import forms
from .models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude = ['user', 'like']

    text_tweet = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                        'placeholder': 'Enter Your Tweet...'}))
    image_tweet = forms.ImageField(label='', required=False)


