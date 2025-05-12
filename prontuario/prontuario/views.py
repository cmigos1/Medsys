from django.shortcuts import render, redirect
from clinica.models import Paciente, Consulta
from django.contrib import messages
from django.db.models import Max

def home(request):
    return render(request, 'home.html')

def pacientes(request):
    pacientes = Paciente.objects.annotate(
        ultima_consulta=Max('consulta__data')
    ).all()
    return render(request, 'pacientes.html', {'pacientes': pacientes})

def consultas(request):
    return render(request, 'consultas.html')

def prontuarios(request):
    return render(request, 'prontuarios.html')

def agenda(request):
    return render(request, 'agenda.html')

def cadastrar_paciente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        
        try:
            Paciente.objects.create(
                nome=nome,
                data_nascimento=data_nascimento,
                cpf=cpf,
                telefone=telefone,
                endereco=endereco
            )
            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('pacientes')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar paciente: {str(e)}')
    
    return render(request, 'cadastrar_paciente.html')
