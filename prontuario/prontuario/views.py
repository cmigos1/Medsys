from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def pacientes(request):
    return render(request, 'pacientes.html')

def consultas(request):
    return render(request, 'consultas.html')

def prontuarios(request):
    return render(request, 'prontuarios.html')

def agenda(request):
    return render(request, 'agenda.html')