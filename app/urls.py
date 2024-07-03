from django.urls import path
from . import views

urlpatterns = [
    path('',views.empty),
    path('login',views.login_view,name='login'),
    path('signup',views.signup,name='signup'),
    path('feed',views.feed,name='feed'),
    path('profile/<str:username>/',views.profile,name='profile'),
    path('profile-settings',views.profile_settings,name='profile-settings'),
    path('logout',views.logout_view,name='logout'),

    path('follow/<str:username>',views.follow,name='follow'),
    path('unfollow/<str:username>',views.unfollow,name='unfollow'),

    path('upload-post',views.upload_post,name='upload-post'),
    path('explore/', views.explore_view, name='explore'),


    path('like-post/',views.like_post,name='like-post'),
    path('comment-post/',views.comment_post,name='comment-post'),
    path('share-post/',views.share_post,name='share-post'),

   ]
