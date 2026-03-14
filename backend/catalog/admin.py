from django.contrib import admin
from .models import Tabela, Coluna, MetricaQualidade

admin.site.register(Tabela)
admin.site.register(Coluna)
admin.site.register(MetricaQualidade)
