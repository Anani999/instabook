from django.urls import path
from . import views

urlpatterns = [
    path('',views.empty),
    path('login',views.login_view,name='login'),
    path('signup',views.signup,name='signup'),
    path('feed',views.feed,name='feed'),
    path('profile',views.profile,name='profile'),
    path('profile-settings',views.profile_settings,name='profile-settings'),
    path('logout',views.logout_view,name='logout')
]
