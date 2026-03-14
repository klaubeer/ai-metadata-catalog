from django.db import models
from pgvector.django import VectorField


class Tabela(models.Model):

    catalogo = models.CharField(max_length=255)
    schema = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)

    descricao = models.TextField(null=True, blank=True)
    responsavel = models.CharField(max_length=255, null=True, blank=True)

    ultima_atualizacao = models.DateTimeField(null=True, blank=True)

    embedding = VectorField(dimensions=1536, null=True)

    def __str__(self):
        return f"{self.schema}.{self.nome}"


class Coluna(models.Model):

    tabela = models.ForeignKey(
        Tabela,
        on_delete=models.CASCADE,
        related_name="colunas"
    )

    nome = models.CharField(max_length=255)
    tipo_dado = models.CharField(max_length=255)

    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.tabela.nome}.{self.nome}"


class MetricaQualidade(models.Model):

    tabela = models.OneToOneField(
        Tabela,
        on_delete=models.CASCADE,
        related_name="qualidade"
    )

    taxa_nulos = models.FloatField()
    taxa_duplicados = models.FloatField()
    quantidade_linhas = models.BigIntegerField()

    ultima_execucao = models.DateTimeField()

    def __str__(self):
        return f"Métricas de qualidade para {self.tabela.nome}"