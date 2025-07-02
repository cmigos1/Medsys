"""
URL configuration for prontuario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home_page'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # URLs de Pacientes
    path('pacientes/', views.pacientes, name='pacientes'),
    path('pacientes/cadastrar/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('pacientes/<int:paciente_id>/', views.visualizar_paciente, name='visualizar_paciente'),
    path('pacientes/<int:paciente_id>/editar/', views.editar_paciente, name='editar_paciente'),
    
    # URLs de Consultas
    path('consultas/', views.consultas, name='consultas'),
    path('consultas/cadastrar/', views.cadastrar_consulta, name='cadastrar_consulta'),
    path('consultas/<int:consulta_id>/', views.visualizar_consulta, name='visualizar_consulta'),
    path('consultas/<int:consulta_id>/editar/', views.editar_consulta, name='editar_consulta'),
    path('consultas/<int:consulta_id>/cancelar/', views.cancelar_consulta, name='cancelar_consulta'),
    path('consultas/<int:consulta_id>/confirmar/', views.confirmar_consulta, name='confirmar_consulta'),
    path('consultas/<int:consulta_id>/espera/', views.colocar_em_espera, name='colocar_em_espera'),
    path('consultas/<int:consulta_id>/finalizar/', views.finalizar_consulta, name='finalizar_consulta'),
    
    # URLs de Prontuários
    path('prontuarios/', views.prontuarios, name='prontuarios'),
    path('prontuarios/cadastrar/', views.cadastrar_prontuario, name='cadastrar_prontuario'),
    path('prontuarios/<int:prontuario_id>/editar/', views.editar_prontuario, name='editar_prontuario'),
    path('prontuarios/<int:prontuario_id>/imprimir/', views.imprimir_prontuario, name='imprimir_prontuario'),
    
    # Agenda
    path('agenda/', views.agenda, name='agenda'),
]