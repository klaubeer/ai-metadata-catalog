# agente/ferramentas.py

import numpy as np
from catalog.models import Tabela, Coluna, MetricaQualidade
from openai import OpenAI
import os

# Cliente OpenAI para gerar embeddings
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# -----------------------------
# Função para gerar embedding
# -----------------------------
def gerar_embedding(texto):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=texto
    )
    return resp.data[0].embedding

# -----------------------------
# Função de busca semântica
# -----------------------------
def buscar_tabelas(query: str, top_k=5):
    """
    Busca as tabelas semanticamente relacionadas à query usando embeddings.
    Retorna uma lista de objetos Tabela.
    """
    # Gera embedding da query
    query_vec = gerar_embedding(query)

    tabelas = Tabela.objects.exclude(embedding=None)
    resultados = []

    for t in tabelas:
        # Calcula similaridade coseno
        vetor = np.array(t.embedding)
        sim = np.dot(vetor, query_vec) / (np.linalg.norm(vetor) * np.linalg.norm(query_vec))
        resultados.append((sim, t))

    # Ordena por similaridade e pega top_k
    resultados.sort(reverse=True, key=lambda x: x[0])
    top_tabelas = [t for _, t in resultados[:top_k]]

    return top_tabelas

# -----------------------------
# Ferramentas para o agente
# -----------------------------

def search_tables(query: str):
    """
    Ferramenta do agente para buscar tabelas semanticamente.
    Retorna lista de dicionários com nome, schema e descrição.
    """
    try:
        resultados = buscar_tabelas(query, top_k=10)
        return [
            {
                "nome": t.nome,
                "schema": t.schema,
                "descricao": t.descricao
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
                "descricao": coluna.descricao
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
            "last_execution": metricas.ultima_execucao
        }

    except Tabela.DoesNotExist:
        return {"erro": f"Tabela '{table_name}' não encontrada"}

    except MetricaQualidade.DoesNotExist:
        return {"erro": f"Métricas de qualidade não encontradas para '{table_name}'"}

    except Exception as e:
        return {"erro": f"Erro ao gerar relatório de qualidade: {str(e)}"}
