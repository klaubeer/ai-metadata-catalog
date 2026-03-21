import os
from openai import OpenAI
from catalog.models import Tabela, Coluna, MetricaQualidade
from catalog.busca import buscar_tabelas as _buscar_tabelas_db

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def search_tables(query: str = "dados"):
    """
    Ferramenta do agente para buscar tabelas semanticamente.
    Usa pgvector (CosineDistance no banco) — eficiente e sem carga em memória.
    """
    try:
        resultados = _buscar_tabelas_db(query, limite=5)
        return [
            {
                "nome": t.nome,
                "schema": t.schema,
                "descricao": t.descricao,
            }
            for t in resultados
        ]
    except Exception as e:
        return {"erro": f"Erro na busca de tabelas: {str(e)}"}


def get_schema(table_name: str):
    """
    Retorna schema (colunas) de uma tabela.
    """
    try:
        tabela = Tabela.objects.get(nome=table_name)
        colunas = Coluna.objects.filter(tabela=tabela)

        return [
            {
                "nome": coluna.nome,
                "tipo": coluna.tipo_dado,
                "descricao": coluna.descricao,
            }
            for coluna in colunas
        ]

    except Tabela.DoesNotExist:
        return {"erro": f"Tabela '{table_name}' não encontrada"}

    except Exception as e:
        return {"erro": f"Erro ao buscar schema: {str(e)}"}


def quality_report(table_name: str):
    """
    Retorna métricas de qualidade da tabela.
    """
    try:
        tabela = Tabela.objects.get(nome=table_name)
        metricas = MetricaQualidade.objects.get(tabela=tabela)

        return {
            "tabela": tabela.nome,
            "null_rate": metricas.taxa_nulos,
            "duplicate_rate": metricas.taxa_duplicados,
            "row_count": metricas.quantidade_linhas,
            "last_execution": metricas.ultima_execucao,
        }

    except Tabela.DoesNotExist:
        return {"erro": f"Tabela '{table_name}' não encontrada"}

    except MetricaQualidade.DoesNotExist:
        return {"erro": f"Métricas de qualidade não encontradas para '{table_name}'"}

    except Exception as e:
        return {"erro": f"Erro ao gerar relatório de qualidade: {str(e)}"}
