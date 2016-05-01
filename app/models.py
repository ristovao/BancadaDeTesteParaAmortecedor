from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Model: Teste
# Utilizada para criacao de uma instancia do teste da bancada
class Teste(models.Model):
	
	teste_id = models.AutoField(primary_key=True)
	teste_nome = models.CharField(max_length=45, null=True)
	teste_tempo_total = models.TimeField(null=True)	
	teste_tempo_oscilacao = models.TimeField(null=True)	
	teste_observacoes = models.TextField(max_length=255, null=True)
	teste_data_hora = models.DateTimeField(default=timezone.now)