from django.urls import path

from messenger.views import *

urlpatterns = [
    path("friends/", FriendsView.as_view(), name="friends"),
    path("profile/upload_avatar", upload_avatar, name="upload-avatar"),
    path("friends/add", AddFriendsView.as_view(), name="friends-add"),
    path("profile/<str:username>", ProfileView.as_view(), name="profile"),
    path("chats/", ChatsView.as_view(), name="chats"),
    path("chats/add", AddChatsView.as_view(), name="chats-add"),
    path("chats/<int:pk>", ChatDetailView.as_view(), name="chats-detailed"),
]
