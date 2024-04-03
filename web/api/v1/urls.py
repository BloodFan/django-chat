from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    path('chat/', include(('api.v1.chat.urls'))),
]
