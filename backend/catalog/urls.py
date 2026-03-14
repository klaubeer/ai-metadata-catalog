from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("<int:tabela_id>/", views.tabela_detalhe, name="tabela_detalhe"),
]
