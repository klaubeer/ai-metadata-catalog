import random

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response

from catalog.busca import buscar_tabelas
from catalog.models import Tabela, Coluna, MetricaQualidade


# -----------------------------------------------
# API - Busca semântica
# -----------------------------------------------

@api_view(["GET"])
def search_tables(request):
    query = request.GET.get("q")

    if not query:
        return Response({"error": "query parameter 'q' is required"}, status=400)

    resultados = buscar_tabelas(query)

    data = [
        {
            "schema": t.schema,
            "nome": t.nome,
            "descricao": t.descricao,
        }
        for t in resultados
    ]

    return Response(data)


# -----------------------------------------------
# API - Refresh de metadados de uma tabela
# -----------------------------------------------

@api_view(["POST"])
def refresh_tabela(request, tabela_id):
    """
    Atualiza os metadados de uma tabela sob demanda.

    Em produção com Databricks, este endpoint chamaria o connector
    (ingestao/databricks_connector.py) para buscar metadados frescos
    diretamente do Unity Catalog.

    Atualmente simula o refresh atualizando timestamps e recalculando métricas.
    """
    tabela = get_object_or_404(Tabela, id=tabela_id)

    tabela.ultima_atualizacao = timezone.now()
    tabela.save()

    metricas, _ = MetricaQualidade.objects.get_or_create(
        tabela=tabela,
        defaults={
            "taxa_nulos": 0,
            "taxa_duplicados": 0,
            "quantidade_linhas": 0,
            "ultima_execucao": timezone.now(),
        },
    )

    metricas.taxa_nulos = round(random.uniform(0, 0.08), 3)
    metricas.taxa_duplicados = round(random.uniform(0, 0.01), 3)
    metricas.quantidade_linhas = random.randint(1000, 100000)
    metricas.ultima_execucao = timezone.now()
    metricas.save()

    return Response({
        "status": "ok",
        "tabela": tabela.nome,
        "ultima_atualizacao": tabela.ultima_atualizacao,
        "metricas": {
            "taxa_nulos": metricas.taxa_nulos,
            "taxa_duplicados": metricas.taxa_duplicados,
            "quantidade_linhas": metricas.quantidade_linhas,
        },
    })


# -----------------------------------------------
# PAGE - Catálogo (lista de tabelas com filtros)
# -----------------------------------------------

def catalogo(request):
    schema_filtro = request.GET.get("schema", "")
    sort = request.GET.get("sort", "nome")

    tabelas = Tabela.objects.select_related("qualidade").all()

    if schema_filtro:
        tabelas = tabelas.filter(schema=schema_filtro)

    sort_map = {
        "nome": "nome",
        "schema": "schema",
        "desatualizada": "ultima_atualizacao",
    }
    tabelas = tabelas.order_by(sort_map.get(sort, "nome"))

    schemas = Tabela.objects.values_list("schema", flat=True).distinct().order_by("schema")

    response = render(
        request,
        "catalogo/lista_tabelas.html",
        {
            "tabelas": tabelas,
            "schemas": schemas,
            "schema_ativo": schema_filtro,
            "sort_ativo": sort,
        },
    )
    response["Cache-Control"] = "no-store"
    return response


# -----------------------------------------------
# PAGE - Detalhe de uma tabela
# -----------------------------------------------

def tabela_detalhe(request, tabela_id):
    tabela = get_object_or_404(Tabela, id=tabela_id)
    colunas = Coluna.objects.filter(tabela_id=tabela.id)

    try:
        qualidade = tabela.qualidade
    except MetricaQualidade.DoesNotExist:
        qualidade = None

    return render(
        request,
        "catalogo/tabela_detalhe.html",
        {
            "tabela": tabela,
            "colunas": colunas,
            "qualidade": qualidade,
        },
    )


# -----------------------------------------------
# PAGE - Dashboard de qualidade
# -----------------------------------------------

def qualidade_dashboard(request):
    metricas = (
        MetricaQualidade.objects
        .select_related("tabela")
        .order_by("-taxa_nulos")
    )

    total = metricas.count()
    criticas = sum(1 for m in metricas if m.taxa_nulos > 0.15 or m.taxa_duplicados > 0.03)
    avg_nulos = round(sum(m.taxa_nulos for m in metricas) / total * 100, 1) if total else 0
    avg_duplicados = round(sum(m.taxa_duplicados for m in metricas) / total * 100, 1) if total else 0

    return render(
        request,
        "catalogo/qualidade_dashboard.html",
        {
            "metricas": metricas,
            "total": total,
            "criticas": criticas,
            "avg_nulos": avg_nulos,
            "avg_duplicados": avg_duplicados,
        },
    )
