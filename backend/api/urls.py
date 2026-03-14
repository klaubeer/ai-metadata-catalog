from django.urls import path
from .views import chat, catalogo, chat_page, home

urlpatterns = [

    path("", home),

    path("chat/", chat_page),

    path("chat-api/", chat),

    path("catalogo/", catalogo),

]