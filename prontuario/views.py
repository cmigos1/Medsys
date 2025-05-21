from django.shortcuts import render, redirect, get_object_or_404
from clinica.models import Paciente, Consulta, Prontuario
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

def visualizar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # Busca todas as consultas do paciente
    consultas = Consulta.objects.filter(
        paciente=paciente
    ).select_related('medico').order_by('-data')
    
    # Busca todos os prontuários do paciente
    prontuarios = Prontuario.objects.filter(
        consulta__paciente=paciente
    ).select_related('consulta', 'consulta__medico').order_by('-consulta__data')
    
    return render(request, 'visualizar_paciente.html', {
        'paciente': paciente,
        'consultas': consultas,
        'prontuarios': prontuarios
    })

def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        try:
            paciente.nome = request.POST.get('nome')
            paciente.data_nascimento = request.POST.get('data_nascimento')
            paciente.cpf = request.POST.get('cpf')
            paciente.telefone = request.POST.get('telefone')
            paciente.endereco = request.POST.get('endereco')
            paciente.save()
            
            messages.success(request, 'Paciente atualizado com sucesso!')
            return redirect('pacientes')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar paciente: {str(e)}')
    
    return render(request, 'editar_paciente.html', {'paciente': paciente})
