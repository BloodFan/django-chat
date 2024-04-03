from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('chats/', views.ChatAPIView.as_view(), name='chats'),
    path('messages/<str:chat_id>/', views.ChatMessageAPIView.as_view(), name='messages'),
    path('init/', views.ChatInitView.as_view(), name='init'),
]
