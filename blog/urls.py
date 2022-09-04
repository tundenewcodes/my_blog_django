from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='homepage'),
    path('posts', views.All_Posts.as_view(),  name='posts'),
    path('read-later', views.Read_later.as_view(),  name='read-later'),
    path('posts/<slug:slug>', views.Unique_Post.as_view(), name='uniquepost'),
]