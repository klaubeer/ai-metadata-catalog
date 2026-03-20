from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("qualidade/", views.qualidade_dashboard, name="qualidade_dashboard"),
    path("<int:tabela_id>/", views.tabela_detalhe, name="tabela_detalhe"),
    path("<int:tabela_id>/refresh/", views.refresh_tabela, name="refresh_tabela"),
]
