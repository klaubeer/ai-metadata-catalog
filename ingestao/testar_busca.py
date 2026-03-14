import os
import sys
import django

sys.path.append("/app/backend")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from catalog.busca import buscar_tabelas


resultados = buscar_tabelas("dados de vendas")

for r in resultados:
    print(r.nome, r.schema)
