"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import TesteTemperatura, TesteTempo

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class TesteTempoForm(forms.ModelForm):

	class Meta:
		model = TesteTempo
		fields = ('teste_nome', 'teste_tempo_total', 'teste_tempo_oscilacao', 
      'teste_observacoes', 'teste_tempo_inicio')

class TesteTemperaturaForm(forms.ModelForm):

  class Meta:
    model = TesteTemperatura
    fields = ('teste_nome', 'teste_tempo_total', 'teste_tempo_oscilacao', 
      'teste_observacoes', 'teste_temperatura_um', 'teste_temperatura_dois')
