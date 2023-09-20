from django import forms
from .models import Tweet, Tag, ReplyTweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude = ['user', 'like', "is_archive"]

    text_tweet = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                        'placeholder': 'Enter Your Tweet...'}))
    image_tweet = forms.ImageField(label='', required=False)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag_word']

    tag_word = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'Enter Your Tag ...'}))


class ReplyTweetForm(forms.ModelForm):
    class Meta:
        model = ReplyTweet
        fields = ['text']
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                  'placeholder': 'Enter Your Reply Tweet...'}))
