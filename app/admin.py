from django.contrib import admin
from app.models import Teste

admin.site.register(Teste)

class TesteAdmin(admin.ModelAdmin):
	model=Teste
	list_display = ['teste_id', 'teste_nome', 'teste_tempo_total', 'teste_tempo_oscilacao', 'teste_observacoes', 'teste_data_hora' ]

