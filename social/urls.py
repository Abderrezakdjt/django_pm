from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('friends/', views.friend_list, name='friend_list'),
    path('friend-requests/', views.friend_requests, name='friend_requests'),
    path('search/', views.search_users, name='search_users'),
    path('notifications/', views.notifications, name='notifications'),
    path('send-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('chat/<int:user_id>/', views.chat_messages, name='chat_messages'),  # هذا مهم
    path('mark-notification/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
]