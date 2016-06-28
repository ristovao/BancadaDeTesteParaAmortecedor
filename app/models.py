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
	amortecedor_diametro_externo = models.FloatField(verbose_name='Tamanho do Diâmetro Externo')
	
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
	amortecedor = models.ForeignKey(Amortecedor, on_delete=models.CASCADE)
	graficoTemperaturaTempo = models.BinaryField(null = True)
	graficoForcaTempo = models.BinaryField(null = True)
	graficoForcaDeslocamento = models.BinaryField(null = True)
	curso = models.FloatField(verbose_name='Tamanho do Curso')

	def getGraficoTemperaturaTempo(self):
		return loads(self.graficoTemperaturaTempo)
		
	def setGraficoTemperaturaTempo(self,lista):
		self.graficoTemperaturaTempo = dumps(lista)
		
	def getGraficoForcaTempo(self):
		return loads(self.graficoForcaTempo)
		
	def setGraficoForcaTempo(self,lista):
		self.graficoForcaTempo = dumps(lista)
		
	def getGraficoForcaDeslocamento(self):
		return loads(self.graficoForcaDeslocamento)
		
	def setrGaficoForcaDeslocamento(self,lista):
		self.graficoForcaDeslocamento = dumps(lista)
	
class TesteVelocidadeFixa(Teste):

	testeVF_velocidade = models.FloatField(null = True, verbose_name='Velocidade do Motor',default=5,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)])	
	
class TesteVelocidadeVariavel(Teste):

	testeVV_quantidade_velocidade = models.IntegerField(null = True, verbose_name='Quantidade de Velocidades')
	arrayVelocidades = models.BinaryField(null = True)
	def getArrayVelocidades(self):
		return loads(self.arrayVelocidades)
		
	def setArrayVelocidades(self,lista):
		self.arrayVelocidades = dumps(lista)

class TesteTemperatura(Teste):

	testeTT_quantidade_temperatura = models.IntegerField(null = True, verbose_name='Quantidade de Temperaturas') 
	testeVV_quantidade_velocidade = models.IntegerField(null = True, verbose_name='Quantidade de Velocidades')	

