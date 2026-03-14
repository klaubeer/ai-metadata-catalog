from openai import OpenAI
from pgvector.django import CosineDistance
from catalog.models import Tabela

client = OpenAI()


def buscar_tabelas(query, limite=5):

    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = resp.data[0].embedding

    resultados = (
        Tabela.objects
        .annotate(distancia=CosineDistance("embedding", query_embedding))
        .order_by("distancia")[:limite]
    )

    return resultados
