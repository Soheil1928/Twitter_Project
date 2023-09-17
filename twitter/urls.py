from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home_page'),
    path('profile_list/', views.ProfileList.as_view(), name='profile_list'),
    path('profile_detail/<int:pk>', views.ProfileDetail.as_view(), name='profile_detail'),
    path('follow/<int:pk>', views.Follow.as_view(), name='follow'),
    path('unfollow/<int:pk>', views.Unfollow.as_view(), name='unfollow'),
    path('like/<int:pk>', views.TweetLike.as_view(), name='like'),
]
