"""bancada URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

#from django.contrib import admin
from datetime import datetime
from django.conf.urls import patterns, url
from app import views as appviews
from app.forms import BootstrapAuthenticationForm
from django.contrib.auth import views as authviews
from django.contrib import admin

urlpatterns = [
    # Gerenciamento de Acesso -ADMIN-
    url(r'^admin/', admin.site.urls),
    
    # Rotas do APP
    url(r'^$', appviews.home, name='home'),
    url(r'^iniciarTesteVelocidadeFixa', appviews.iniciarTesteVelocidadeFixa, name='iniciarTesteVelocidadeFixa'),
    url(r'^iniciarTesteVelocidadeVariavel', appviews.iniciarTesteVelocidadeVariavel, name='iniciarTesteVelocidadeVariavel'),
    url(r'^iniciarTesteTemperatura', appviews.iniciarTesteTemperatura, name='iniciarTesteTemperatura'),
    url(r'^historico', appviews.historico, name='historico'),    
    url(r'^amortecedorHistorico', appviews.amortecedorHistorico, name='amortecedorHistorico'),
    url(r'^teste/(?P<primary_key>[0-9]+)/$', appviews.detalharTeste, name='detalharTeste'),
    url(r'^json/amortecedor/(?P<primary_key>[\w\d\.]+)', appviews.pegarDadosAmortecedor, name='jsonAmortecedor'),
    url(r'^json/nomeAmortecedor', appviews.pegarNomesAmortecedor, name='jsonNomesAmortecedor'),
    #url(r'^detalhamento', appviews.detalhamento, name='detalhamento'),
    url(r'^grafico', appviews.grafico, name='grafico'),


    url(r'^login/$',
        authviews.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        authviews.logout,
        {
            'next_page': '/',
        },
        name='logout'),
]
