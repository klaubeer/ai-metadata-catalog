"""
Databricks Unity Catalog Connector
===================================

Script pronto para integração com a API REST do Databricks Unity Catalog.

COMO ATIVAR:
  1. Defina as variáveis de ambiente no docker-compose.yml ou .env:

       DATABRICKS_HOST=https://<workspace>.azuredatabricks.net
       DATABRICKS_TOKEN=<personal-access-token>
       DATABRICKS_CATALOG=<nome-do-catalogo>   (ex: main,)

  2. Execute a ingestão:
       docker exec -it catalog_backend python ingestao/databricks_connector.py

  3. Gere os embeddings após a ingestão:
       docker exec -it catalog_backend python ingestao/gerar_embeddings.py

ATENÇÃO:
  Este script NÃO está conectado a nenhum ambiente Databricks.
  Os dados do catálogo atual foram gerados sinteticamente via gerar_metadados.py.
  Para uso em produção, configure as variáveis de ambiente acima.
"""

import os
import sys
import django
import requests
from datetime import datetime

sys.path.append("/app/backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from catalog.models import Tabela, Coluna, MetricaQualidade

# -----------------------------------------------
# Configuração — lida de variáveis de ambiente
# -----------------------------------------------

DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN")
DATABRICKS_CATALOG = os.environ.get("DATABRICKS_CATALOG", "main")


def get_headers():
    return {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json",
    }


# -----------------------------------------------
# Consultas à API Unity Catalog
# -----------------------------------------------

def listar_schemas():
    """Lista todos os schemas do catálogo configurado."""
    url = f"{DATABRICKS_HOST}/api/2.1/unity-catalog/schemas"
    resp = requests.get(
        url,
        headers=get_headers(),
        params={"catalog_name": DATABRICKS_CATALOG},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("schemas", [])


def listar_tabelas(schema_name):
    """Lista todas as tabelas de um schema."""
    url = f"{DATABRICKS_HOST}/api/2.1/unity-catalog/tables"
    resp = requests.get(
        url,
        headers=get_headers(),
        params={
            "catalog_name": DATABRICKS_CATALOG,
            "schema_name": schema_name,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("tables", [])


def obter_detalhes_tabela(full_name):
    """Retorna metadados completos de uma tabela (colunas, owner, updated_at)."""
    url = f"{DATABRICKS_HOST}/api/2.1/unity-catalog/tables/{full_name}"
    resp = requests.get(url, headers=get_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


# -----------------------------------------------
# Ingestão no catálogo local
# -----------------------------------------------

def ingerir_tabela(detalhes):
    """
    Cria ou atualiza uma tabela no catálogo local
    a partir dos metadados retornados pela API do Databricks.
    """
    full_name = detalhes.get("full_name", "")
    partes = full_name.split(".")
    schema = partes[1] if len(partes) >= 2 else "default"
    nome = partes[2] if len(partes) >= 3 else full_name

    updated_at_ms = detalhes.get("updated_at")
    ultima_atualizacao = (
        datetime.fromtimestamp(updated_at_ms / 1000)
        if updated_at_ms
        else datetime.utcnow()
    )

    tabela, created = Tabela.objects.update_or_create(
        catalogo=DATABRICKS_CATALOG,
        schema=schema,
        nome=nome,
        defaults={
            "descricao": detalhes.get("comment") or "",
            "responsavel": detalhes.get("owner") or "",
            "ultima_atualizacao": ultima_atualizacao,
        },
    )

    # Recria colunas para garantir sincronização
    tabela.colunas.all().delete()
    for col in detalhes.get("columns", []):
        Coluna.objects.create(
            tabela=tabela,
            nome=col.get("name", ""),
            tipo_dado=col.get("type_name", ""),
            descricao=col.get("comment") or "",
        )

    status = "criada" if created else "atualizada"
    return tabela, status


def ingerir_catalogo():
    """
    Ponto de entrada principal.
    Percorre todos os schemas e tabelas do Unity Catalog
    e ingere os metadados no catálogo local.
    """
    if not DATABRICKS_HOST or not DATABRICKS_TOKEN:
        raise EnvironmentError(
            "\n[ERRO] Variáveis de ambiente não configuradas.\n"
            "Defina DATABRICKS_HOST e DATABRICKS_TOKEN antes de executar.\n"
            "Consulte o cabeçalho deste arquivo para instruções detalhadas."
        )

    print(f"Conectando ao catálogo '{DATABRICKS_CATALOG}' em {DATABRICKS_HOST}...")

    schemas = listar_schemas()
    print(f"  {len(schemas)} schemas encontrados.\n")

    total_criadas = 0
    total_atualizadas = 0

    for schema in schemas:
        schema_name = schema.get("name")
        tabelas = listar_tabelas(schema_name)
        print(f"  Schema '{schema_name}': {len(tabelas)} tabela(s)")

        for tabela_resumo in tabelas:
            full_name = tabela_resumo.get("full_name")
            try:
                detalhes = obter_detalhes_tabela(full_name)
                _, status = ingerir_tabela(detalhes)
                if status == "criada":
                    total_criadas += 1
                else:
                    total_atualizadas += 1
            except Exception as e:
                print(f"    [AVISO] Erro ao ingerir '{full_name}': {e}")

    print(
        f"\nIngestão concluída."
        f"\n  Tabelas criadas:     {total_criadas}"
        f"\n  Tabelas atualizadas: {total_atualizadas}"
        f"\n  Total:               {total_criadas + total_atualizadas}"
    )
    print("\nPróximo passo: rode gerar_embeddings.py para indexar busca semântica.")


# -----------------------------------------------
# Execução principal
# -----------------------------------------------

if __name__ == "__main__":
    ingerir_catalogo()
