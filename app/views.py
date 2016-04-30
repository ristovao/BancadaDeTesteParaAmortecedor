from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required


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

@login_required
def iniciarTeste(request):
    """Renders the  page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/iniciarTeste.html',
        context_instance = RequestContext(request,
        {
            'title':'Iniciar teste',
            'message':'',
            'year':datetime.now().year,
        })
    )

def historico(request):
    """Renders the  page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/historico.html',
        context_instance = RequestContext(request,
        {
            'title':'Historico',
            'message':'',
            'year':datetime.now().year,
        })
    )

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