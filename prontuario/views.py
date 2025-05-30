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
<<<<<<< HEAD
    return render(request, 'pacientes.html', {'pacientes': pacientes})

def consultas(request):
    consultas = Consulta.objects.select_related('paciente', 'medico', 'medico__especialidade').order_by('data')
    return render(request, 'consultas.html', {'consultas': consultas})
=======
    return render(request, 'pacientes/pacientes.html', {'pacientes': pacientes})

def consultas(request):
    consultas = Consulta.objects.select_related('paciente', 'medico', 'medico__especialidade').order_by('data')
    return render(request, 'consultas/consultas.html', {'consultas': consultas})
>>>>>>> teste

def prontuarios(request):
    search = request.GET.get('search', '')
    prontuarios = Prontuario.objects.select_related(
        'consulta__paciente', 
        'consulta__medico', 
        'consulta__medico__especialidade'
    ).all()
    
    if search:
        prontuarios = prontuarios.filter(
            consulta__paciente__nome__icontains=search
        )
    
    prontuarios = prontuarios.order_by('-consulta__data')
    
<<<<<<< HEAD
    return render(request, 'prontuarios.html', {
=======
    return render(request, 'prontuario/prontuarios.html', {
>>>>>>> teste
        'prontuarios': prontuarios
    })

def agenda(request):
<<<<<<< HEAD
    return render(request, 'agenda.html')
=======
    return render(request, 'agenda/agenda.html')
>>>>>>> teste

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
    
<<<<<<< HEAD
    return render(request, 'cadastrar_paciente.html')
=======
    return render(request, 'pacientes/cadastrar_paciente.html')
>>>>>>> teste

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
    
<<<<<<< HEAD
    return render(request, 'visualizar_paciente.html', {
=======
    return render(request, 'pacientes/visualizar_paciente.html', {
>>>>>>> teste
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
    
<<<<<<< HEAD
    return render(request, 'editar_paciente.html', {'paciente': paciente})
=======
    return render(request, 'pacientes/editar_paciente.html', {'paciente': paciente})
>>>>>>> teste

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
<<<<<<< HEAD
    return render(request, 'cadastrar_consulta.html', {
=======
    return render(request, 'consultas/cadastrar_consulta.html', {
>>>>>>> teste
        'pacientes': pacientes,
        'medicos': medicos
    })

def visualizar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta.objects.select_related(
        'paciente', 'medico', 'medico__especialidade'
    ), id=consulta_id)
    
<<<<<<< HEAD
    return render(request, 'visualizar_consulta.html', {'consulta': consulta})
=======
    return render(request, 'consultas/visualizar_consulta.html', {'consulta': consulta})
>>>>>>> teste

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
<<<<<<< HEAD
    return render(request, 'editar_consulta.html', {
=======
    return render(request, 'consultas/editar_consulta.html', {
>>>>>>> teste
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

def cadastrar_prontuario(request):
    if request.method == 'POST':
        try:
            consulta_id = request.POST.get('consulta')
            diagnostico = request.POST.get('diagnostico')
            anotacoes = request.POST.get('anotacoes')
            prescricao = request.POST.get('prescricao')
            
            consulta = get_object_or_404(Consulta, id=consulta_id)
            
            Prontuario.objects.create(
                consulta=consulta,
                diagnostico=diagnostico,
                anotacoes=anotacoes,
                prescricao=prescricao
            )
            
            messages.success(request, 'Prontuário criado com sucesso!')
            return redirect('prontuarios')
        except Exception as e:
            messages.error(request, f'Erro ao criar prontuário: {str(e)}')
    
    # Buscar apenas consultas que não têm prontuário
    consultas_sem_prontuario = Consulta.objects.filter(
        prontuario__isnull=True,
        status='CONFIRMADA'
    ).select_related('paciente', 'medico', 'medico__especialidade')
    
<<<<<<< HEAD
    return render(request, 'cadastrar_prontuario.html', {
=======
    return render(request, 'prontuario/cadastrar_prontuario.html', {
>>>>>>> teste
        'consultas': consultas_sem_prontuario
    })

def editar_prontuario(request, prontuario_id):
    prontuario = get_object_or_404(Prontuario, id=prontuario_id)
    
    if request.method == 'POST':
        try:
            prontuario.diagnostico = request.POST.get('diagnostico')
            prontuario.anotacoes = request.POST.get('anotacoes')
            prontuario.prescricao = request.POST.get('prescricao')
            prontuario.save()
            
            messages.success(request, 'Prontuário atualizado com sucesso!')
            return redirect('prontuarios')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar prontuário: {str(e)}')
    
<<<<<<< HEAD
    return render(request, 'editar_prontuario.html', {
=======
    return render(request, 'prontuario/editar_prontuario.html', {
>>>>>>> teste
        'prontuario': prontuario
    })

def imprimir_prontuario(request, prontuario_id):
    prontuario = get_object_or_404(Prontuario, id=prontuario_id)
<<<<<<< HEAD
    return render(request, 'imprimir_prontuario.html', {
=======
    return render(request, 'prontuario/imprimir_prontuario.html', {
>>>>>>> teste
        'prontuario': prontuario
    })
