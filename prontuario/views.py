from django.shortcuts import render, redirect, get_object_or_404
from clinica.models import Paciente, Consulta, Prontuario, Medico
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
    consultas = Consulta.objects.select_related('paciente', 'medico', 'medico__especialidade').order_by('data')
    return render(request, 'consultas.html', {'consultas': consultas})

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

def cadastrar_consulta(request):
    if request.method == 'POST':
        try:
            paciente_id = request.POST.get('paciente')
            medico_id = request.POST.get('medico')
            data = request.POST.get('data')
            motivo = request.POST.get('motivo')
            
            paciente = get_object_or_404(Paciente, id=paciente_id)
            medico = get_object_or_404(Medico, id=medico_id)
            
            Consulta.objects.create(
                paciente=paciente,
                medico=medico,
                data=data,
                motivo=motivo
            )
            
            messages.success(request, 'Consulta agendada com sucesso!')
            return redirect('consultas')
        except Exception as e:
            messages.error(request, f'Erro ao agendar consulta: {str(e)}')
    
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.select_related('especialidade').all()
    return render(request, 'cadastrar_consulta.html', {
        'pacientes': pacientes,
        'medicos': medicos
    })

def visualizar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta.objects.select_related(
        'paciente', 'medico', 'medico__especialidade'
    ), id=consulta_id)
    
    return render(request, 'visualizar_consulta.html', {'consulta': consulta})

def editar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    if request.method == 'POST':
        try:
            consulta.paciente_id = request.POST.get('paciente')
            consulta.medico_id = request.POST.get('medico')
            consulta.data = request.POST.get('data')
            consulta.motivo = request.POST.get('motivo')
            consulta.status = request.POST.get('status')
            consulta.save()
            
            messages.success(request, 'Consulta atualizada com sucesso!')
            return redirect('consultas')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar consulta: {str(e)}')
    
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.select_related('especialidade').all()
    return render(request, 'editar_consulta.html', {
        'consulta': consulta,
        'pacientes': pacientes,
        'medicos': medicos
    })

def cancelar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    if request.method == 'POST':
        try:
            consulta.status = 'CANCELADA'
            consulta.save()
            messages.success(request, 'Consulta cancelada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao cancelar consulta: {str(e)}')
    
    return redirect('consultas')
