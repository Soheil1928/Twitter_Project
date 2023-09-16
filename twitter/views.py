from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from .models import Tweet
from .forms import TweetForm


class Home(View):
    def get(self, request):
        user_tweets = Tweet.objects.all().order_by('-create_at')
        if request.user.is_authenticated:
            form = TweetForm()
            context = {'user_tweets': user_tweets, 'form': form}
            return render(request, 'twitter/home_page.html', context)
        else:
            return render(request, 'twitter/home_page.html', {'user_tweets': user_tweets})

    def post(self, request):
        if request.user.is_authenticated:
            form = TweetForm(request.POST, request.FILES)
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()

                messages.success(request, 'Your Twit Has Been Posted!...', 'success')
                return redirect('home_page')

            user_tweets = Tweet.objects.all().order_by('-create_at')
            return render(request, 'twitter/home_page.html', {'user_tweets': user_tweets,
                                                              'form': form})
        else:
            user_tweets = Tweet.objects.all().order_by('-create_at')
            return render(request, 'twitter/home_page.html', {'user_tweets': user_tweets})
