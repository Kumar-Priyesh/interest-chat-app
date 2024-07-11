from django.urls import path, include
from .views import register_view, login_view, logout_view, index_view, user_list_view, received_interests_view, chat_list_view, chat_view, accept_interest_view, send_message_view
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'interests', InterestViewSet, basename='interest')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', index_view, name='index'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', user_list_view, name='user_list'),
    path('received_interests/', received_interests_view, name='received_interests'),
    path('chats/', chat_list_view, name='chat_list'),
    path('chat/<int:interest_id>/', chat_view, name='chat'),
    path('api/', include(router.urls)),
    
    path('accept_interest/<int:interest_id>/', accept_interest_view, name='accept_interest'),
    path('send_message/<int:interest_id>/', send_message_view, name='send_message'),

    path('send_request/<int:user_id>/', send_request_view, name='send_request'),

    # path('ws/chat/<str:room_name>/', views.ChatConsumer.as_asgi(), name='ws_chat'),
   
]
