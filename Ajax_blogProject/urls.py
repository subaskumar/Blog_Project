"""Ajax_blogProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from testApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.post_list_view,),
    path('signup/', views.sinUp_view, name='signUp'),
    path('Login/', views.login_view, name='login'),
    path('LogOut/', views.logout_view, name='logout'),
    path('searched/', views.search_venue,name ='searched'),
    path('edit_myProfile/', views.edit_profile, name='updateProfile'),
    path('<int:id>/my_profile/', views.userProfile, name='myProfile'),
    path('<int:id>/delete/', views.DeleteComment, name='delete'),
    path('<int:pk>/like_comment/', views.AddLike_comment, name='likes_comment'),
    path('<int:id>/updateComment/', views.UpdateComment, name='updateComment'),
    path('verification/', include('verify_email.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),     # it includes login,logout...etc
    path('<int:pk>/like/', views.AddLike, name='like'),
    path('<int:pk>/dislike/', views.AddDislike, name='dislike'),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<post>[\w-]+)/$',views.post_detail_view,name='post_detail'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view() ,name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view() ,name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view() ,name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view() ,name='password_reset_complete'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view() ,name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view() ,name='password_change_done'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
