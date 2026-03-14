import os
import sys
import django
from openai import OpenAI

sys.path.append("/app/backend")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from catalog.models import Tabela, Coluna  # adiciona Coluna

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def gerar_embedding(texto):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=texto
    )
    return resp.data[0].embedding

def gerar_embeddings():
    tabelas = Tabela.objects.all()

    for tabela in tabelas:
        # texto base com nome, schema e descrição (mantendo o que já existia)
        texto = f"""
        tabela {tabela.nome}
        schema {tabela.schema}
        descricao {tabela.descricao}
        """

        # adicionar nomes das colunas ao texto para melhorar similaridade
        colunas = Coluna.objects.filter(tabela=tabela)
        if colunas.exists():
            nomes_colunas = " ".join([c.nome for c in colunas])
            texto += f" colunas {nomes_colunas}"

        # gerar embedding
        embedding = gerar_embedding(texto)
        tabela.embedding = embedding
        tabela.save()

        print(f"embedding atualizado: {tabela.nome}")

if __name__ == "__main__":
    gerar_embeddings()
