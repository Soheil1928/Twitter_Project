from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from django.views.generic.list import ListView
from .models import Tweet
from .forms import TweetForm
from accounts.models import Profile


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


class ProfileList(View):
    def get(self, request):
        if request.user.is_authenticated:
            profiles = Profile.objects.exclude(user=request.user)
            return render(request, 'twitter/profile_list.html', {'profiles': profiles})
        else:
            messages.error(request, 'You Must Be Logged In View This Page ...', 'danger')
            return redirect('home_page')


class ProfileDetail(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user_id=pk)
            tweets = Tweet.objects.filter(user_id=pk).order_by('-create_at')
            return render(request, 'twitter/profile_detail.html', {'profile': profile, 'tweets': tweets})

    def post(self, request, pk):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user_id=pk)
            tweets = Tweet.objects.filter(user_id=pk).order_by('-create_at')
            current_user_profile = request.user.profile
            action = request.POST['follow_name']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
                current_user_profile.save()
            elif action == 'follow':
                current_user_profile.follows.add(profile)
                current_user_profile.save()

            return render(request, 'twitter/profile_detail.html', {'profile': profile, 'tweets': tweets})
        else:
            messages.error(request, 'You Must Be Logged In View This Page ...', 'danger')
            return redirect('home_page')


class Follow(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user_id=pk)
            request.user.profile.follows.add(profile)
            request.user.profile.save()
            messages.success(request, f'You Have Successfully Followed {profile.user.username}', 'success')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'That User Dose Not Exist...!', 'danger')
            return redirect('home_page')


class Unfollow(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user_id=pk)
            request.user.profile.follows.remove(profile)
            request.user.profile.save()
            messages.success(request, f'You Have Successfully Unfollowed {profile.user.username}', 'success')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'That User Dose Not Exist...!', 'danger')
            return redirect('home_page')


class TweetLike(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            tweet = get_object_or_404(Tweet, id=pk)
            if tweet.like.filter(id=request.user.id):
                tweet.like.remove(request.user)
            else:
                tweet.like.add(request.user)
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            messages.error(request, 'You Must Be Logged In View This Page ...', 'danger')
            return redirect('home_page')


class Follower(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            if request.user.id == pk:
                profile: Profile = Profile.objects.get(user_id=pk)
                return render(request, 'twitter/follows.html', {'profile': profile})
            else:
                messages.error(request, "That's Not Your Profile Page", 'danger')
                return redirect('home_page')
        else:
            messages.success(request, "You Must Be logged To View That Page...", 'danger')
            return redirect('home_page')


class Following(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            if request.user.id == pk:
                profile: Profile = Profile.objects.get(user_id=pk)
                return render(request, 'twitter/following.html', {'profile': profile})
            else:
                messages.error(request, "That's Not Your Profile Page", 'danger')
                return redirect('home_page')
        else:
            messages.success(request, "You Must Be logged To View That Page...", 'danger')
            return redirect('home_page')


class DeleteTweet(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            tweet = get_object_or_404(Tweet, id=pk)
            if request.user.id == tweet.user.id:
                tweet.delete()
                messages.success(request, "The Tweet Has Been Deleted", 'success')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "You Don't Own That tweet!", 'danger')
                return redirect('home_page')

        else:
            messages.error(request, 'Please Login To Continue...!', 'danger')
            return redirect(request.META.get('HTTP_REFERER'))


class SearchUser(View):
    def get(self, request):
        return render(request, 'twitter/search_user.html')

    def post(self, request):
        search = request.POST['search_user']
        search_db = User.objects.filter(username__contains=search)
        return render(request, 'twitter/search_user.html', {'search_db': search_db})


class SearchTweet(View):
    def get(self, request):
        return render(request, 'twitter/search_tweet.html')

    def post(self, request):
        search = request.POST['search_tweet']
        search_db = Tweet.objects.filter(text_tweet__contains=search)
        return render(request, 'twitter/search_tweet.html', {'search_db': search_db})
