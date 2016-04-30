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

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', appviews.home, name='home'),
    url(r'^iniciarTeste$', appviews.iniciarTeste, name='iniciarTeste'),
    url(r'^historico', appviews.historico, name='historico'),
    url(r'^grafico', appviews.grafico, name='grafico'),
    url(r'^teste', appviews.teste, name='teste'),
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
