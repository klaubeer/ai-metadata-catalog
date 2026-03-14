import os
import sys
import django
import random
from datetime import datetime

# adicionar backend ao PYTHONPATH
sys.path.append("/app/backend")

# configurar django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from catalog.models import Tabela, Coluna, MetricaQualidade

# ------------------------
# Configurações do POC
# ------------------------

DOMINIOS = [
    "sales",
    "logistics",
    "inventory",
    "marketing",
    "production"
]

COLUNAS_PADRAO = [
    ("id", "integer"),
    ("created_at", "timestamp"),
    ("updated_at", "timestamp"),
]

TIPOS_ADICIONAIS = ["integer", "float", "text", "date"]

DESCRICOES = [
    "Identificador único",
    "Data de criação",
    "Data de atualização",
    "Valor monetário",
    "Nome do cliente",
    "Código do produto",
    "Flag ativo",
]

# ------------------------
# Funções de geração
# ------------------------

def gerar_colunas(tabela):
    """Gera colunas padrão + adicionais com tipos e descrições"""
    total = random.randint(4, 8)

    # Colunas padrão
    for nome, tipo in COLUNAS_PADRAO:
        Coluna.objects.create(
            tabela=tabela,
            nome=nome,
            tipo_dado=tipo,
            descricao="Campo padrão do sistema"
        )

    # Colunas adicionais
    for i in range(total):
        Coluna.objects.create(
            tabela=tabela,
            nome=f"campo_{i}",
            tipo_dado=random.choice(TIPOS_ADICIONAIS),
            descricao=random.choice(DESCRICOES)
        )

def gerar_tabelas():
    """Gera tabelas sintéticas com colunas e métricas de qualidade"""
    for dominio in DOMINIOS:
        for i in range(20):
            nome_tabela = f"{dominio}_table_{i}"

            tabela = Tabela.objects.create(
                catalogo="main",
                schema=dominio,
                nome=nome_tabela,
                descricao=f"Tabela de dados do domínio {dominio}",
                responsavel="data_team",
                ultima_atualizacao=datetime.utcnow()
            )

            gerar_colunas(tabela)

            MetricaQualidade.objects.create(
                tabela=tabela,
                taxa_nulos=round(random.uniform(0, 0.2), 3),
                taxa_duplicados=round(random.uniform(0, 0.05), 3),
                quantidade_linhas=random.randint(1000, 100000),
                ultima_execucao=datetime.utcnow()
            )

# ------------------------
# Execução principal
# ------------------------

if __name__ == "__main__":
    gerar_tabelas()
    print("Metadados gerados com sucesso")
