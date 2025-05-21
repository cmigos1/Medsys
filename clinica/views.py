from django.shortcuts import render

from prontuario.clinica.models import Paciente



# Create your views here.

def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'clinica/lista_pacientes.html', {'pacientes': pacientes})