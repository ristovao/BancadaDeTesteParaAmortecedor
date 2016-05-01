from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import TesteTemperaturaForm, TesteTempoForm
from .models import Teste, TesteTempo, TesteTemperatura


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

#@login_required
#def iniciarTeste(request):
#    """Renders the  page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/iniciarTeste.html',
#        context_instance = RequestContext(request,
#        {
#            'title':'Iniciar teste',
#            'message':'',
#            'year':datetime.now().year,
#        })
#    )

#def historico(request):
#    """Renders the  page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/historico.html',
#        context_instance = RequestContext(request,
#        {
#            'title':'Historico',
#            'message':'',
#            'year':datetime.now().year,
#        })
#    )

def grafico(request):
    """Renders the  page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/grafico.html',
        context_instance = RequestContext(request,
        {
            'title':'Grafico',
            'message':'',
            'year':datetime.now().year,
        })
    )
    
@login_required
def teste(request):
    """Renders the  page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/teste.html',
        context_instance = RequestContext(request,
        {
            'title':'Teste',
            'message':'',
            'year':datetime.now().year,
        })
    )

def iniciarTeste(request):
    
    page = 'app/iniciarTeste.html'

    if request.method == "POST":
        form = TesteTempoForm(request.POST)
        
        if form.is_valid():
            teste = form.save(commit=False)
            teste.teste_nome = request.POST['teste_nome']
            teste.teste_tempo_total = request.POST['teste_tempo_total']
            teste.teste_tempo_oscilacao = request.POST['teste_tempo_oscilacao']
            teste.teste_observacoes = request.POST['teste_observacoes']
            teste.teste_tempo_inicio = request.POST['teste_tempo_inicio']
            teste.save()
            return redirect('/grafico')

    else:
        form = TesteTempoForm()
    
    return render(request, page, {'form':form})

def iniciarTesteTemperatura(request):
    
    page = 'app/iniciarTesteTemperatura.html'

    if request.method == "POST":
        form = TesteTemperaturaForm(request.POST)
        
        if form.is_valid():
            teste = form.save(commit=False)
            teste.teste_nome = request.POST['teste_nome']
            teste.teste_tempo_total = request.POST['teste_tempo_total']
            teste.teste_tempo_oscilacao = request.POST['teste_tempo_oscilacao']
            teste.teste_observacoes = request.POST['teste_observacoes']
            teste.teste_temperatura_um = request.POST['teste_temperatura_um']
            teste.teste_temperatura_dois = request.POST['teste_temperatura_dois']
            teste.save()
            return redirect('/grafico')

    else:
        form = TesteTemperaturaForm()
    
    return render(request, page, {'form':form})

def historico(request):
    
    page = 'app/historico.html'

    lista_de_testes = Teste.objects.order_by('teste_id')

    return render(request, page, {'lista_de_testes': lista_de_testes})