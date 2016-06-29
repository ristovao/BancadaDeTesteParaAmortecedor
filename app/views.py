from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import AmortecedorForm, TesteVelocidadeFixaForm, TesteVelocidadeVariavelForm, TesteTemperaturaForm, UnknownForm
from .models import Amortecedor, Teste, TesteVelocidadeFixa, TesteVelocidadeVariavel, TesteTemperatura
from django.contrib.sessions.models import Session
from importlib import import_module
from django.conf import settings
import random
from itertools import chain
import socket



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    #if len(Session.objects.all())>1:
    #    session = Session.objects.all()[1]
    #    session.delete()
    #    return render(request,'app/jaLogado.html')

    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )  

def sobre(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    #if len(Session.objects.all())>1:
    #    session = Session.objects.all()[1]
    #    session.delete()
    #    return render(request,'app/jaLogado.html')

    return render(
        request,
        'app/sobre.html',
        context_instance = RequestContext(request,
        {
            'title':'Sobre a Bancada',
            'year':datetime.now().year,
        })
    )

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
    teste_current  = list(chain(TesteTemperatura.objects.filter(teste_id=primary_key),TesteVelocidadeFixa.objects.filter(teste_id=primary_key),TesteVelocidadeVariavel.objects.filter(teste_id=primary_key)))
    teste_current = teste_current[0]
    teste_current.graficoTemp = str(teste_current.getGraficoTemperaturaTempo())
    teste_current.graficoForcaDeslocamento = str(teste_current.getGraficoForcaDeslocamento())
    teste_current.graficoForcaTempo = str(teste_current.getGraficoForcaTempo())
    return render(request, page, {'detalhamento_do_teste': teste_current})

def detalharAmortecedor(request, primary_key):
    page = 'app/detalhamentoamortecedor.html'

    amortecedor = get_object_or_404(Amortecedor, amortecedor_id=primary_key)
    amortecedor_testes = list(Teste.amortecedor.filter(amortecedor_codigo=amortecedor.amortecedor_codigo))

    return render(request, page, {'amortecedor_testes': amortecedor_testes})

@login_required
def iniciarTesteVelocidadeFixa(request):
    
    page = 'app/iniciarTesteVelocidadeFixa.html'

    if request.method == "POST":
        form = TesteVelocidadeFixaForm(request.POST)
        formArm = AmortecedorForm(request.POST)
        if 'amortecedor_codigo' in request.POST :
            amortecedorList = Amortecedor.objects.filter(amortecedor_codigo=request.POST['amortecedor_codigo'])
            if len(amortecedorList):
                amortecedor = amortecedorList[0]
                formArm = AmortecedorForm(request.POST, instance=amortecedor)
            
        if form.is_valid() and formArm.is_valid():
            teste = form.save(commit=False)
            if len(amortecedorList):
                teste.amortecedor=amortecedor
            else:
                amortecedor = formArm.save(commit=False)
                amortecedor.amortecedor_codigo = request.POST['amortecedor_codigo']
                amortecedor.amortecedor_diametro_externo = request.POST['amortecedor_diametro_externo']
                amortecedor.save()
                teste.amortecedor=amortecedor
            teste.teste_nome = request.POST['teste_nome']
            teste.testeVF_velocidade = request.POST['testeVF_velocidade']
            teste.teste_quantidade_ciclo = request.POST['teste_quantidade_ciclo']
            teste.teste_observacoes = request.POST['teste_observacoes']
            teste.curso = request.POST['curso']
            listaDeValores = pegarValores(teste.teste_quantidade_ciclo)
            teste.setGraficoTemperaturaTempo(listaDeValores)
            listaDeValores = pegarValores(teste.teste_quantidade_ciclo)
            teste.setGraficoForcaTempo(listaDeValores)
            listaDeValores = pegarValores(teste.teste_quantidade_ciclo)
            teste.setrGaficoForcaDeslocamento(listaDeValores)
            teste.save()
            return redirect('app.views.detalharTeste', primary_key=teste.pk)

    else:
        form = TesteVelocidadeFixaForm()
        formArm = AmortecedorForm()
    
    return render(request, page, {'form':form, 'formArm':formArm})

@login_required
def iniciarTesteVelocidadeVariavel(request):
    
    page = 'app/iniciarTesteVelocidadeVariavel.html'

    if request.method == "POST":
        form = TesteVelocidadeVariavelForm(request.POST)
        choices=[]
        if 'choices1' in request.POST:
            choices.append(request.POST['choices1'])
        if 'choices2' in request.POST:
            choices.append(request.POST['choices2'])
        if 'choices3' in request.POST:
            choices.append(request.POST['choices3'])
        
        if len(choices)==0:
            form.erroChoice = "Selecione uma velocidade"
            formArm = AmortecedorForm()
            return render(request, page, {'form':form, 'formArm':formArm})

            
        formArm = AmortecedorForm(request.POST)
        if 'amortecedor_codigo' in request.POST :
            amortecedorList = Amortecedor.objects.filter(amortecedor_codigo=request.POST['amortecedor_codigo'])
            if len(amortecedorList):
                amortecedor = amortecedorList[0]
                formArm = AmortecedorForm(request.POST, instance=amortecedor)
        
        if form.is_valid() and formArm.is_valid():
            
            
            
            teste = form.save(commit=False)
            if len(amortecedorList):
                teste.amortecedor=amortecedor
            else:
                amortecedor = formArm.save(commit=False)
                amortecedor.amortecedor_codigo = request.POST['amortecedor_codigo']
                amortecedor.amortecedor_diametro_externo = request.POST['amortecedor_diametro_externo']
                amortecedor.save()
                teste.amortecedor=amortecedor
            teste.teste_nome = request.POST['teste_nome']
            teste.testeVV_quantidade_velocidade = len(choices)
            teste.curso = 10
            teste.setArrayVelocidades(choices)
            teste.teste_quantidade_ciclo = request.POST['teste_quantidade_ciclo']
            teste.teste_observacoes = request.POST['teste_observacoes']
            listaDeValores = pegarValores(teste.teste_quantidade_ciclo)
            teste.setGraficoTemperaturaTempo(listaDeValores)
            listaDeValores = pegarValores(teste.teste_quantidade_ciclo)
            teste.setGraficoForcaTempo(listaDeValores)
            listaDeValores = pegarValores(teste.teste_quantidade_ciclo)
            teste.setrGaficoForcaDeslocamento(listaDeValores)
            teste.save()
            return redirect('app.views.detalharTeste', primary_key=teste.pk)

    else:
        form = TesteVelocidadeVariavelForm()
        formArm = AmortecedorForm()
    return render(request, page, {'form':form, 'formArm':formArm})

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

def amortecedorHistorico(request):

    page = 'app/historicoAmortecedor.html'

    lista_de_amortecedores = Amortecedor.objects.order_by('amortecedor_codigo')

    return render(request, page, {'lista_de_amortecedores': lista_de_amortecedores})
    
def grafico(request):
    page='app/grafico.html'
    
    return render(request, page,{})

@login_required
def pegarDadosAmortecedor(request,primary_key):
    dados={}
    amortecedor = Amortecedor.objects.filter(amortecedor_codigo=primary_key)
    if not(len(amortecedor)):
        dados={'erro':1}
    else:
        d=amortecedor[0]
        dados['amortecedor_diametro_externo']=str(d.amortecedor_diametro_externo)
        #dados['amortecedor_curso']=str(d.amortecedor_curso)
    
    return JsonResponse(dados)

@login_required
def pegarNomesAmortecedor(request):
    dados={'nomes':[]}
    amortecedor = Amortecedor.objects.all()
    if (len(amortecedor)):
        for i in amortecedor:
            dados['nomes'].append(i.amortecedor_codigo)
    
    return JsonResponse(dados)



#funcao de teste para pegar valores de algum lugar
def pegarValores(quant):
    BUFFER_SIZE=10000
    while 1:
        try:
            #clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #clientsocket.connect(('localhost', 4567))
            #temp = clientsocket.send('hello')
            #g = clientsocket.recv(3)
            #g = g.decode("utf-8") 
            #g = g.split(",")
            #g = map(int,g)
            #g = list(g)
            f = []
            for i in range(int(quant)):
                f.append([random.randint(0,90),i])
            break
        except:
            pass
    return f
            

