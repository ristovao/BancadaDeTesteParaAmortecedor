from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import AmortecedorForm, TesteVelocidadeFixaForm, TesteVelocidadeVariavelForm, UnknownForm
from .models import Amortecedor, Teste, TesteVelocidadeFixa, TesteVelocidadeVariavel
from django.contrib.sessions.models import Session
from importlib import import_module
from django.conf import settings
import random
from itertools import chain
import socket
import time



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
    teste_current  = list(chain(TesteVelocidadeFixa.objects.filter(teste_id=primary_key),TesteVelocidadeVariavel.objects.filter(teste_id=primary_key)))
    teste_current = teste_current[0]
    teste_current.graficoForcaDeslocamento = str(teste_current.getGraficoForcaDeslocamento())
    teste_current.graficoForcaTempo = str(teste_current.getGraficoForcaTempo())
    return render(request, page, {'detalhamento_do_teste': teste_current})

def detalharAmortecedor(request, primary_key):
    page = 'app/detalhamentoamortecedor.html'

    amortecedor = get_object_or_404(Amortecedor, amortecedor_codigo=primary_key)
    amortecedor_testes = list(chain(TesteVelocidadeFixa.objects.filter(amortecedor=amortecedor),TesteVelocidadeVariavel.objects.filter(amortecedor=amortecedor)))

    return render(request, page, {'amortecedor_testes':amortecedor_testes, 'amortecedor_atual':amortecedor})

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
<<<<<<< HEAD
            listaDeValores = pegarValores2(teste.curso, teste.testeVF_velocidade, teste.teste_quantidade_ciclo)
            teste.setGraficoTemperaturaTempo(listaDeValores)
            listaDeValores = pegarValores2(teste.curso, teste.testeVF_velocidade, teste.teste_quantidade_ciclo)
            teste.setGraficoForcaTempo(listaDeValores)
            listaDeValores = pegarValores2(teste.curso, teste.testeVF_velocidade, teste.teste_quantidade_ciclo)
            teste.setrGaficoForcaDeslocamento(listaDeValores)
=======
            listaDeValores = pegarValores(teste.teste_quantidade_ciclo)
            tempo = listaDeValores[0]
            velocidade = listaDeValores[1]
            temperatura = listaDeValores[2]
            forca = listaDeValores[3]
            teste.setGraficoTemperaturaTempo(temperatura)
            teste.setGraficoForcaTempo(forca)
            teste.setrGaficoForcaDeslocamento(velocidade)
>>>>>>> f397c1cfc221aa09d3fb76e728e8e8cc17e5f5b9
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
            teste.curso = request.POST['curso']
            teste.setArrayVelocidades(choices)
            teste.teste_quantidade_ciclo = request.POST['teste_quantidade_ciclo']
            teste.teste_observacoes = request.POST['teste_observacoes']
            listaDeValores = pegarValores2(teste.curso, teste.testeVV_quantidade_velocidade, teste.teste_quantidade_ciclo)
            teste.setGraficoTemperaturaTempo(listaDeValores)
            listaDeValores = pegarValores2(teste.curso, teste.testeVV_quantidade_velocidade, teste.teste_quantidade_ciclo)
            teste.setGraficoForcaTempo(listaDeValores)
            listaDeValores = pegarValores2(teste.curso, teste.testeVV_quantidade_velocidade, teste.teste_quantidade_ciclo)
            teste.setrGaficoForcaDeslocamento(listaDeValores)
            teste.save()
            return redirect('app.views.detalharTeste', primary_key=teste.pk)

    else:
        form = TesteVelocidadeVariavelForm()
        formArm = AmortecedorForm()
    return render(request, page, {'form':form, 'formArm':formArm})

def historico(request):
    
    page = 'app/historico.html'

    lista_de_testes = list(chain(TesteVelocidadeFixa.objects.all(),TesteVelocidadeVariavel.objects.all()))

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

#função responsável por selecionar um teste
def selecionaTeste(curso, velocidade, ciclo):
    codigo = 0
    curso_um = 10
    curso_dois = 12.5 
    curso_tres = 15
    velocidade_um = 175
    velocidade_dois = 200
    velocidade_tres = 225
    ciclo_um = 10
    ciclo_dois =  20
    ciclo_tres = 30
    if(curso == curso_um):
        if(velocidade == velocidade_um):
            if(ciclo == ciclo_um):
                codigo = 1
            elif(ciclo == ciclo_dois):
                codigo = 2
            elif(ciclo == ciclo_tres):
                codigo = 3
        elif(velocidade == velocidade_dois):
            if(ciclo == ciclo_um):
                codigo = 4
            elif(ciclo == ciclo_dois):
                codigo = 5
            elif(ciclo == ciclo_tres):
                codigo = 6
        elif(velocidade == velocidade_tres):
            if(ciclo == ciclo_um):
                codigo = 7
            elif(ciclo == ciclo_dois):
                codigo = 8
            elif(ciclo == ciclo_tres):
                codigo = 9
    elif(curso == curso_dois):
        if(velocidade == velocidade_um):
            if(ciclo == ciclo_um):
                codigo = 10
            elif(ciclo == ciclo_dois):
                codigo = 11
            else:
                codigo = 12
        elif(velocidade == velocidade_dois):
            if(ciclo == ciclo_um):
                codigo = 13
            elif(ciclo == ciclo_dois):
                codigo = 14
            elif(ciclo == ciclo_tres):
                codigo = 15
        elif(velocidade == velocidade_tres):
            if(ciclo == ciclo_um):
                codigo = 16
            elif(ciclo == ciclo_dois):
                codigo = 17
            elif(ciclo == ciclo_tres):
                codigo = 18
    elif(curso == curso_tres):
        if(velocidade == velocidade_um):
            if(ciclo == ciclo_um):
                codigo = 19
            elif(ciclo == ciclo_dois):
                codigo = 20
            else:
                codigo = 21
        elif(velocidade == velocidade_dois):
            if(ciclo == ciclo_um):
                codigo = 22
            elif(ciclo == ciclo_dois):
                codigo = 23
            elif(ciclo == ciclo_tres):
                codigo = 24
        elif(velocidade == velocidade_tres):
            if(ciclo == ciclo_um):
                codigo = 25
            elif(ciclo == ciclo_dois):
                codigo = 26
            elif(ciclo == ciclo_tres):
                codigo = 27    
    return codigo

#funcao de teste para pegar valores de algum lugar
def pegarValores(curso, velocidade, ciclo):
    #BUFFER_SIZE=10000
    g = ""
    while 1:
        try:
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.connect(('192.168.1.47', 8765))
            temp = clientsocket.send('1')
            time.sleep(0.25)
            temp = clientsocket.recv(10000)
            g = temp
            while('\n\n' not in temp):
                g=g+temp
                temp = clientsocket.recv(10000)
            #g = g.decode("utf-8") 
            g = g.split("\n")
            #g = map(int,g)
            #g = list(g)
            #f = []
            #for i in range(int(quant)):
            #    f.append([random.randint(0,90),i])
            break
        except:
            pass
    tempo=[]
    velocidade=[]
    temperatura=[]
    forca=[]
    for i in g:
        if i:
            tempo.append(i.split('\t')[0])
            velocidade.append(i.split('\t')[1])
            temperatura.append(i.split('\t')[2])
            forca.append(i.split('\t')[3])
    saida=[]
    saida.append(list(map(float,[x for x in tempo if x])))
    saida.append(list(map(float,[x for x in velocidade if x])))
    saida.append(list(map(float,[x for x in temperatura if x])))
    saida.append(list(map(float,[x for x in forca if x])))
    return saida

def pegarValores2(curso, velocidade, ciclo):
    #BUFFER_SIZE=10000
    g = ""
    while 1:
        try:
            #clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #clientsocket.connect(('localhost', 8765))
            #temp = clientsocket.send('1')
            #temp = clientsocket.recv(10000)
            #while(temp):
            #    g=g+temp
            #    temp = clientsocket.recv(10000)
            ##g = g.decode("utf-8") 
            #g = g.split("\n")
            ##g = map(int,g)
            ##g = list(g)
            f = []
            for i in range(int(quant)):
                f.append([random.randint(0,90),i])
            break
        except:
            pass
    return f            

