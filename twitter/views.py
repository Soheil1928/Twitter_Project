from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Tweet, Tag, ReplyTweet
from .forms import TweetForm, TagForm, ReplyTweetForm
from accounts.models import Profile


class Home(View):
    def get(self, request):
        user_tweets = Tweet.objects.filter(is_archive=False).order_by('-create_at')
        main_reply_list = ReplyTweet.objects.filter(parent=None)
        reply_reply_list = ReplyTweet.objects.filter(parent=not None)
        if request.user.is_authenticated:
            form = TweetForm()
            context = {'user_tweets': user_tweets,
                       'form': form,
                       'main_reply_list': main_reply_list,
                       'reply_reply_list': reply_reply_list}
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
                form.save_m2m()

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
            tweets = Tweet.objects.filter(user_id=pk, is_archive=False).order_by('-create_at')
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
        search_db = Tweet.objects.filter(text_tweet__contains=search, is_archive=False)
        return render(request, 'twitter/search_tweet.html', {'search_db': search_db})


def edit_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username == tweet.user.username:
            form = TweetForm(request.POST or None, request.FILES or None, instance=tweet)
            if request.method == 'POST':
                if form.is_valid():
                    edit = form.save(commit=False)
                    edit.user = request.user
                    edit.save()
                    form.save_m2m()
                    messages.success(request, 'Your Twit Has Been Updated!...', 'success')
                    return redirect('home_page')
            else:
                return render(request, 'twitter/edit_tweet.html', {'form': form, 'tweet': tweet})
        else:
            messages.error(request, "You Don't Own That twit!", 'danger')
            return redirect('home_page')
    else:
        messages.error(request, 'Please Login To Continue...!', 'danger')
        return redirect('home_page')


class Archive(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            tweet_archive = Tweet.objects.get(id=pk)

            if not tweet_archive.is_archive:
                tweet_archive.is_archive = True
                tweet_archive.save()

            elif tweet_archive.is_archive:
                tweet_archive.is_archive = False
                tweet_archive.save()

            return redirect(request.META.get('HTTP_REFERER'))

        else:
            messages.error(request, 'Please Login To Continue...!', 'danger')
            return redirect('home_page')


class ArchivePage(View):
    def get(self, request):
        if request.user.is_authenticated:
            tweet_archive = Tweet.objects.filter(is_archive=True)
            if tweet_archive:
                return render(request, 'twitter/archive_page.html', {'tweet_archive': tweet_archive})
            else:
                messages.warning(request, 'You Have No Archived Tweets...!', 'warning')
                return redirect('home_page')
        else:
            messages.error(request, 'Please Login To Continue...!', 'danger')
            return redirect('home_page')


class TweetTag(View):
    def get(self, request):
        if request.user.is_authenticated:
            tags = Tag.objects.all()
            tag_form = TagForm()
            return render(request, 'twitter/tweet_tag.html', {'tag_form': tag_form, 'tags': tags})
        else:
            messages.error(request, 'You Must Be Logged In View This Page ...', 'danger')
            return redirect('home_page')

    def post(self, request):
        if request.user.is_authenticated:
            tag_form = TagForm(request.POST)
            if tag_form.is_valid():
                tag_form.save()
                messages.success(request, 'Your Tags Submitted ...', 'success')
                return render(request, 'twitter/tweet_tag.html', {'tag_form': tag_form})
            else:
                return redirect(request.META.get('HTTP_REFERER'))

        else:
            messages.error(request, 'You Must Be Logged In View This Page ...', 'danger')
            return redirect('home_page')


class ReplyTweetView(View):
    def get(self, request, tweet_id):
        if request.user.is_authenticated:
            reply_tweet_form = ReplyTweetForm()
            tweet = Tweet.objects.get(id=tweet_id)
            return render(request, 'twitter/reply_tweet_page.html', {'reply_tweet_form': reply_tweet_form,
                                                                     'tweet': tweet})

    def post(self, request, tweet_id):
        if request.user.is_authenticated:
            reply_tweet_form = ReplyTweetForm(request.POST)
            if reply_tweet_form.is_valid():
                reply_form = reply_tweet_form.save(commit=False)
                reply_tweet = ReplyTweet(tweet_id=tweet_id, parent=None, text=reply_form, user_id=request.user.id)
                reply_tweet.save()
                return redirect('home_page')


class ReplyReplyView(View):
    def get(self, request, tweet_id, parent_id):
        reply_reply_form = ReplyTweetForm()
        reply = ReplyTweet.objects.get(tweet_id=tweet_id, id=parent_id)
        return render(request, 'twitter/reply_reply_page.html', {'reply_reply_form': reply_reply_form,
                                                                 'reply': reply})

    def post(self, request, tweet_id, parent_id):
        reply_reply_form = ReplyTweetForm(request.POST)
        if reply_reply_form.is_valid():
            reply = ReplyTweet(tweet_id=tweet_id,
                               parent_id=parent_id,
                               user_id=request.user.id,
                               text=reply_reply_form.cleaned_data.get('text'))
            reply.save()
        return redirect('home_page')
