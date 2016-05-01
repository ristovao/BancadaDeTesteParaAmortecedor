from django.contrib import admin
from app.models import Teste, TesteTempo, TesteTemperatura

admin.site.register(TesteTempo)
admin.site.register(TesteTemperatura)

class TesteAdmin(admin.ModelAdmin):
	model=Teste
	list_display = ['teste_id', 'teste_nome', 'teste_tempo_total', 'teste_tempo_oscilacao', 'teste_observacoes', 'teste_data_hora' ]


class TesteTemperaturaAdmin(admin.ModelAdmin):
	model = TesteTempo
	list_display = ['teste_inicio']

class TesteTempoAdmin(admin.ModelAdmin):
	model = TesteTemperatura
	list_display = ['teste_temperatura_um', 'teste_temperatura_dois']