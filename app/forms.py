"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import TesteVelocidadeFixa, TesteVelocidadeVariavel, TesteTemperatura, Amortecedor

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

class TesteVelocidadeFixaForm(forms.ModelForm):

  class Meta:
    model = TesteVelocidadeFixa
    #fields = '__all__'
    #exclude = ['teste_data_hora']   
    fields = ('teste_id', 'teste_nome', 'teste_quantidade_ciclo', 'testeVF_velocidade', 'teste_observacoes', 'curso')


class TesteVelocidadeVariavelForm(forms.ModelForm):

  class Meta:
    model = TesteVelocidadeVariavel
    fields = ('amortecedor', 'teste_id', 'teste_nome', 'teste_quantidade_ciclo', 'teste_observacoes',)


class TesteTemperaturaForm(forms.ModelForm):

  class Meta:
    model = TesteTemperatura
    fields = ('amortecedor', 'teste_id', 'teste_nome', 'teste_quantidade_ciclo', 'teste_observacoes', 'teste_data_hora', 'testeTT_quantidade_temperatura', 'testeVV_quantidade_velocidade')


class AmortecedorForm(forms.ModelForm):

  class Meta:
    model = Amortecedor
    fields = ('amortecedor_codigo', 'amortecedor_diametro_externo')

class UnknownForm(forms.Form):
    choices = forms.MultipleChoiceField(
        choices = (
                  ('10.0', '10'),
                  ('12.5', '12.5'),
                  ('15.0', '15'),
                 ), # this is optional
        widget  = forms.CheckboxSelectMultiple,
    )