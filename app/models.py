# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from pickle import loads, dumps
from django.core.validators import MaxValueValidator, MinValueValidator

# Model: Amortecedor
# Utilizada para cardar informações do Amortecedor	
class Amortecedor (models.Model):

	#amortecedor_id = models.AutoField(primary_key=True, verbose_name='ID do Amortecedor')
	amortecedor_codigo = models.CharField(max_length=45, primary_key=True, verbose_name='Código') 
	amortecedor_diametro_externo = models.IntegerField(verbose_name='Tamanho do Diâmetro Externo')
	amortecedor_curso = models.IntegerField(verbose_name='Tamanho do Curso')

	def __repr__(self):
		return self.amortecedor_codigo
	def __str__(self):
		return self.amortecedor_codigo

# Model: Teste
# Utilizada para criacao de uma instancia do teste da bancada
class Teste(models.Model):
		
	teste_id = models.AutoField(primary_key=True, verbose_name='ID')
	teste_nome = models.CharField(max_length=45, null = False, verbose_name='Nome')
	teste_quantidade_ciclo = models.IntegerField(null = True, verbose_name='Quantidade de Ciclo',default=5,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)])
	teste_observacoes = models.TextField(max_length=255, null = True, verbose_name='Observações')
	teste_data_hora = models.DateTimeField(default=timezone.now, verbose_name='Data')
	#graficos = models.ForeignKey(Grafico, verbose_name='Gráficos', on_delete=models.CASCADE)
	amortecedor = models.ForeignKey(Amortecedor, on_delete=models.CASCADE)
	graficoTemperatura = models.BinaryField(null = True)
	graficoForcaTempo = models.BinaryField(null = True)
	graficoMimimi = models.BinaryField(null = True)
	def getGraficoTemperatura(self):
		return loads(self.graficoTemperatura)
		
	def setGraficoTemperatura(self,lista):
		self.graficoTemperatura = dumps(lista)
	
class TesteVelocidadeFixa(Teste):

	testeVF_velocidade = models.IntegerField(null = True, verbose_name='Velocidade do Motor',default=5,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)])	
	
class TesteVelocidadeVariavel(Teste):

	testeVV_quantidade_velocidade = models.IntegerField(null = True, verbose_name='Quantidade de Velocidades')
	arrayVelocidades = models.BinaryField(null = True)
	#FALTA: array das velocidade(s)
	def getArrayVelocidades(self):
		return loads(self.arrayVelocidades)
		
	def setArrayVelocidades(self,lista):
		self.arrayVelocidades = dumps(lista)

class TesteTemperatura(Teste):

	testeTT_quantidade_temperatura = models.IntegerField(null = True, verbose_name='Quantidade de Temperaturas') 
	#FALTA: array de temperatura(s)
	testeVV_quantidade_velocidade = models.IntegerField(null = True, verbose_name='Quantidade de Velocidades')	
	#FALTA: array das velocidade(s)




# Model: Grafico
# Utilizada para criação dos gráficos resultantes da realização dos testes
class Grafico (models.Model):
	teste = models.ForeignKey(Teste, verbose_name='Teste', on_delete=models.CASCADE)
	
	