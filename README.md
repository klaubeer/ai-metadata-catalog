Demo online: https://predict-fill-link-continuity.trycloudflare.com/

# Data Navigator

Plataforma de **catálogo de metadados com suporte de IA** que permite que analistas descubram datasets, entendam seus schemas e consultem metadados usando linguagem natural.

O sistema organiza metadados em um catálogo central e permite consulta através de:

- navegação no catálogo
- busca semântica
- agente conversacional

O objetivo é permitir **descoberta de dados self-service**, reduzindo dependência do time de dados.

---

# Problema

Ambientes de dados corporativos normalmente possuem **centenas de tabelas**.

Problemas comuns:

- analistas não sabem quais datasets existem
- metadados são incompletos
- o time de dados recebe muitas perguntas repetidas
- datasets duplicados acabam sendo criados

O objetivo do projeto é permitir que analistas consigam **descobrir e entender datasets sem depender do time de dados**.

---

# Solução

Criar um **AI Metadata Catalog** que:

1. ingere metadados do ambiente de dados  
2. organiza essas informações em um catálogo central  
3. gera descrições automáticas com IA  
4. permite busca semântica de datasets  
5. oferece um agente conversacional para consulta de metadados  

Assim analistas conseguem descobrir datasets existentes **sem abrir chamados para o time de dados**.

---

# Arquitetura do Sistema

Fluxo de alto nível:

```

Data Platform
↓
Metadata Ingestion
↓
PostgreSQL (pgvector)
↓
Catalog API
↓
Agent com Tools
↓
Interface Web

```

Arquitetura baseada em um catálogo central de metadados enriquecido com IA.

---

# Funcionalidades Implementadas

## Catálogo de datasets

Interface web para explorar tabelas disponíveis.

Permite:

- visualizar lista de tabelas
- navegar por schema
- ver descrição da tabela
- visualizar colunas
- ver tipos de dados
- visualizar métricas básicas de qualidade

---

## Página de detalhe da tabela

Mostra:

- schema
- colunas
- tipos de dados
- descrição do dataset
- métricas de qualidade

---

## Busca semântica

O sistema permite pesquisar datasets usando linguagem natural.

A busca utiliza **embeddings vetoriais** armazenados no banco.

---

## Agente conversacional

O sistema inclui um agente de IA capaz de responder perguntas sobre os datasets.

O agente utiliza **tools específicas** para acessar o catálogo.

Tools disponíveis:

```

search_tables
get_schema
quality_report

```

Essas ferramentas permitem recuperar informações estruturadas sobre tabelas.

---

## Chat com o catálogo

Interface de chat integrada ao agente.

Exemplos de perguntas:

```

quais tabelas possuem dados de vendas?
qual o schema da tabela sales_orders?
quais datasets estão desatualizados?

```

---

# Ingestão de Metadados

Scripts de ingestão populam o catálogo com metadados.

No POC os dados são **gerados sinteticamente** para simular um ambiente real com aproximadamente 100 tabelas.

Metadados gerados:

- catalog
- schema
- table name
- columns
- data types
- owner
- last update

Também são geradas:

- métricas básicas de qualidade
- embeddings para busca semântica

---

# Métricas de Qualidade

O sistema calcula indicadores simples de qualidade de dados:

- null_rate
- duplicate_rate
- row_count
- last update

Essas métricas ajudam a entender a confiabilidade do dataset.

---



---

# Stack Tecnológica

Backend

- Python
- Django
- Django REST Framework

Banco de dados

- PostgreSQL
- pgvector

IA

- OpenAI
- LangChain

Frontend

- Django Templates

Infraestrutura

- Docker
- Docker Compose

Ambiente de desenvolvimento

- Python 3.11+

---

# Como rodar o projeto

## 1. Clonar repositório

```

git clone <repo>
cd ai-metadata-catalog

```

## 2. Subir containers

```

docker-compose up --build

```

## 3. Rodar ingestão de metadados

```

docker exec -it catalog_backend python ingestao/gerar_metadados.py

```

## 4. Gerar embeddings

```

docker exec -it catalog_backend python ingestao/gerar_embeddings.py

```


```


```

O sistema já permite demonstrar:

- AI Data Discovery
- Semantic Search
- Conversational Data Catalog
- Schema Exploration
- Metadata Quality Insights

---

# Objetivo do Projeto

Este projeto demonstra experiência prática em:

- data platforms
- data governance
- vector search
- LLM agents
- metadata catalog
- backend engineering

Além de reproduzir um problema comum em empresas que utilizam grandes ambientes de dados.
