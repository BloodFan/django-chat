from django.urls import path

from main.views import TemplateAPIView

urlpatterns = [
    path('main/', TemplateAPIView.as_view(template_name='chat/main.html'), name='main'),
    path('init/', TemplateAPIView.as_view(template_name='chat/chat.html'), name='init'),
]
