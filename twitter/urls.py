from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home_page'),
    path('profile_list/', views.ProfileList.as_view(), name='profile_list'),
    path('profile_detail/<int:pk>', views.ProfileDetail.as_view(), name='profile_detail'),
    path('profile_detail/follower/<int:pk>', views.Follower.as_view(), name='follower'),
    path('profile_detail/following/<int:pk>', views.Following.as_view(), name='following'),
    path('follow/<int:pk>', views.Follow.as_view(), name='follow'),
    path('unfollow/<int:pk>', views.Unfollow.as_view(), name='unfollow'),
    path('like/<int:pk>', views.TweetLike.as_view(), name='like'),
    path('delete_tweet/<int:pk>', views.DeleteTweet.as_view(), name='delete_tweet'),
    path('search_user/', views.SearchUser.as_view(), name='search_user'),
    path('search_tweet/', views.SearchTweet.as_view(), name='search_tweet'),
    path('edit_tweet/<int:pk>', views.edit_tweet, name='edit_tweet'),
    path('archive_tweet/<int:pk>', views.Archive.as_view(), name='archive_tweet'),
    path('archive_page/', views.ArchivePage.as_view(), name='archive_page'),
    path('tweet_tag/', views.TweetTag.as_view(), name='tweet_tag'),
    path('reply_tweet/<int:tweet_id>', views.ReplyTweetView.as_view(), name='reply_tweet'),
    path('reply_reply/<int:tweet_id>/<int:parent_id>', views.ReplyReplyView.as_view(), name='reply_reply'),
]
