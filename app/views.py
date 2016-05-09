from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import AmortecedorForm, TesteVelocidadeFixaForm, TesteVelocidadeVariavelForm, TesteTemperaturaForm
from .models import Amortecedor, Teste, TesteVelocidadeFixa, TesteVelocidadeVariavel, TesteTemperatura
from django.contrib.sessions.models import Session
from importlib import import_module
from django.conf import settings

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    if len(Session.objects.all())>1:
        session = Session.objects.all()[1]
        session.delete()
        return render(request,'app/jaLogado.html')

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
    

#@login_required
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

def detalharTeste(request, primary_key):
    
    page = 'app/detalhamento.html'
    teste_current = get_object_or_404(Teste, teste_id=primary_key)

    return render(request, page, {'detalhamento_do_teste': teste_current})


@login_required
def iniciarTeste(request):
    
    page = 'app/iniciarTeste.html'

    if request.method == "POST":
        form = TesteVelocidadeFixaForm(request.POST)
        
        if form.is_valid():
            teste = form.save(commit=False)
            teste.teste_nome = request.POST['teste_nome']
            teste.teste_quantidade_ciclo = request.POST['teste_quantidade_ciclo']
            teste.teste_observacoes = request.POST['teste_observacoes']
            
            teste.save()
            return redirect('app.views.detalharTeste', primary_key=teste.pk)

    else:
        form = TesteVelocidadeFixaForm()
    
    return render(request, page, {'form':form})

@login_required
def iniciarTesteTemperatura(request):
    
    page = 'app/iniciarTesteTemperatura.html'

    if request.method == "POST":
        form = TesteTemperaturaForm(request.POST)
        
        if form.is_valid():
            teste = form.save(commit=False)
            teste.teste_nome = request.POST['teste_nome']
            teste.teste_observacoes = request.POST['teste_observacoes']
            
            teste.save()
            return redirect('app.views.detalharTeste', primary_key=teste.pk)

    else:
        form = TesteTemperaturaForm()
    
    return render(request, page, {'form':form})

def historico(request):
    
    page = 'app/historico.html'

    lista_de_testes = Teste.objects.order_by('teste_id')

    return render(request, page, {'lista_de_testes': lista_de_testes})