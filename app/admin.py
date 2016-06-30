from django.contrib import admin
from app.models import Amortecedor, Teste, TesteVelocidadeFixa, TesteVelocidadeVariavel

admin.site.register(Amortecedor)
admin.site.register(TesteVelocidadeVariavel)
admin.site.register(TesteVelocidadeFixa)

class AmortecedorAdmin(admin.ModelAdmin):
	model = Amortecedor
	list_display = ['amortecedor_id', 'amortecedor_codigo', 'amortecedor_diametro_externo', 'amortecedor_curso']

class TesteAdmin(admin.ModelAdmin):
	model=Teste
	list_display = ['teste_id', 'teste_nome', 'teste_quantidade_ciclo', 'teste_observacoes', 'teste_data_hora', 'amortecedor']

class TesteVelocidadeFixaAdmin(admin.ModelAdmin):
	model = TesteVelocidadeFixa
	list_display = ['testeVF_velocidade']

class TesteVelocidadeVariavelAdmin(admin.ModelAdmin):
	model = TesteVelocidadeVariavel
	list_display = ['testeVV_quantidade_velocidade']
