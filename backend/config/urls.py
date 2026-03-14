from django.contrib import admin
from django.urls import path, include
from catalog.views import search_tables
from api.views import chat  # importa a view do chat

urlpatterns = [
    path("admin/", admin.site.urls),

    # páginas da aplicação
    path("", include("api.urls")),

    # catálogo
    path("catalogo/", include("catalog.urls")),

    # endpoint de busca
    path("api/search/", search_tables),

    # endpoint do chat
    path("api/chat-api/", chat),  
]
