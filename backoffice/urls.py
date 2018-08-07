from django.urls import re_path

from . import views

app_name = 'backoffice'
urlpatterns = [
    re_path(r'^$', views.dashboard, name='dashboard'),
    re_path(r'^my_post', views.view_user_post, name='user_post'),
    re_path(r'^all_post', views.view_all_post, name='all_post'),
    re_path(r'^post/comment/(\d+)', views.commentpost, name='comment_post'),
    re_path(r'^post/comment/delete/(\d+)', views.deletecomment, name='delete_post'),
    re_path(r'^post/like/(\d+)', views.likepost, name='like_post'),
    re_path(r'^post/(\d+)', views.displaypost, name='display_post'),
    re_path(r'^post/delete/(\d+)', views.deletepost, name='delete_post'),
    re_path(r'^profile/(\d+)', views.profile, name='profile')
]
