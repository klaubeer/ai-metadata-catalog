from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render, get_object_or_404

from catalog.busca import buscar_tabelas
from catalog.models import Tabela, Coluna


@api_view(["GET"])
def search_tables(request):

    query = request.GET.get("q")

    if not query:
        return Response({"error": "query parameter 'q' is required"}, status=400)

    resultados = buscar_tabelas(query)

    data = []

    for tabela in resultados:
        data.append({
            "schema": tabela.schema,
            "nome": tabela.nome,
            "descricao": tabela.descricao
        })

    return Response(data)


def catalogo(request):

    tabelas = Tabela.objects.all().order_by("schema", "nome")

    return render(
        request,
        "catalogo/lista_tabelas.html",
        {
            "tabelas": tabelas
        }
    )


def tabela_detalhe(request, tabela_id):

    tabela = get_object_or_404(Tabela, id=tabela_id)

    colunas = Coluna.objects.filter(tabela_id=tabela.id)

    return render(
        request,
        "catalogo/tabela_detalhe.html",
        {
            "tabela": tabela,
            "colunas": colunas
        }
    )
