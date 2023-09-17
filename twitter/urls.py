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
]
