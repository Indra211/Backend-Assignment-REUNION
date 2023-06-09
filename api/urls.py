from django.urls import path
from.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    )


urlpatterns =[
    path('authenticate/', TokenObtainPairView.as_view(), name='user_authenticate'),
    path("follow/<int:pk>",follow_user,name="followers"),
    path('unfollow/<int:pk>/',unfollow_user,name='followers'),
    path('user/',get_user_profile,name='users'),
    path('posts/',posts,name='posts'),
    path("posts/<int:pk>/",delete_post,name = 'delete_post'),
    path('like/<int:pk>/',like_post,name='like'),
    path('unlike/<int:pk>/',unlike_post,name='unlike'),
    path('comment/<int:pk>/',add_comment,name='comment'),
    path('posts/<int:pk>/',get_post_details,name='post_detail'),
    path('all_posts/',get_all_posts,name='posts'),
    path('set_cookie/', set_cookie_view, name='set_cookie'),
    path('get_cookie/', get_cookie_view, name='get_cookie'),
    path('delete_cookie/', delete_cookie_view, name='delete_cookie'),
]