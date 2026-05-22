from django.urls import path
from .views import *

urlpatterns = [
    path('', chatbot_page, name='chatbot'),
    path('api/', chatbot_api, name='chatbot_api'),

    path('history/', history_page, name='history'),
    path('get-messages/<int:conv_id>/', get_messages, name='get_messages'),

    path('delete/<int:conv_id>/', delete_conversation, name='delete_chat'),
    path('rename/', rename_conversation, name='rename_chat'),
]