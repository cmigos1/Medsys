from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Max
from django.utils import timezone
from datetime import datetime, timedelta
from clinica.models import *
from .decorators import *

def home_page(request):
    """Landing page do sistema"""
    return render(request, 'home.html')

def login_view(request):
    """View de login com autenticação real"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Login realizado com sucesso como {user.get_user_type_display()}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    
    return render(request, 'auth/login.html')

@login_required
def logout_view(request):
    """Logout do usuário"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('home_page')

@all_authenticated_required
def dashboard(request):
    """Dashboard com dados específicos por tipo de usuário"""
    user = request.user
    hoje = timezone.now().date()
    
    # Determinar tipo de usuário (considerando superuser como admin)
    if user.is_superuser or (hasattr(user, 'user_type') and user.user_type == 'admin'):
        user_type_display = 'admin'
    elif hasattr(user, 'user_type') and user.user_type == 'medico':
        user_type_display = 'medico'
    else:
        user_type_display = 'recepcionista'
    
    context = {
        'user_type': user_type_display,
        'username': user.get_full_name() or user.username,
        'is_admin': user.is_superuser or (hasattr(user, 'user_type') and user.user_type == 'admin'),
        'is_medico': hasattr(user, 'user_type') and user.user_type == 'medico',
        'is_recepcionista': not (user.is_superuser or (hasattr(user, 'user_type') and user.user_type in ['admin', 'medico'])),
    }
    
    if user_type_display == 'admin':
        # Dados completos para administradores
        try:
            context.update({
                'total_pacientes': Paciente.objects.count(),
                'total_medicos': Medico.objects.count(),
                'consultas_hoje': Consulta.objects.filter(data__date=hoje).count(),
                'consultas_pendentes': Consulta.objects.filter(status='PENDENTE').count(),
                'total_prontuarios': Prontuario.objects.count(),
                'consultas_recentes': Consulta.objects.select_related('paciente', 'medico').order_by('-data')[:5],
                'medicos_ativos': Medico.objects.filter(user__is_active=True).count(),
                'total_usuarios': User.objects.count(),
                'usuarios_ativos': User.objects.filter(is_active=True).count(),
            })
        except Exception as e:
            print(f"Erro ao carregar dados do admin: {e}")
            context.update({
                'total_pacientes': 0,
                'total_medicos': 0,
                'consultas_hoje': 0,
                'consultas_pendentes': 0,
                'total_prontuarios': 0,
                'consultas_recentes': [],
                'medicos_ativos': 0,
                'total_usuarios': 0,
                'usuarios_ativos': 0,
            })
    
    elif user_type_display == 'medico':
        # Dados específicos para médicos (apenas suas consultas)
        try:
            medico = user.medico_profile
            consultas_medico = Consulta.objects.filter(medico=medico)
            
            context.update({
                'total_pacientes_medico': consultas_medico.values('paciente').distinct().count(),
                'consultas_hoje_medico': consultas_medico.filter(data__date=hoje).count(),
                'proximas_consultas_medico': consultas_medico.filter(
                    data__date=hoje, 
                    data__time__gte=timezone.now().time()
                ).count(),
                'total_prontuarios_medico': Prontuario.objects.filter(consulta__medico=medico).count(),
                'consultas_medico_hoje': consultas_medico.filter(data__date=hoje).order_by('data')[:5],
                'ultimos_prontuarios_medico': Prontuario.objects.filter(
                    consulta__medico=medico
                ).order_by('-consulta__data')[:5]
            })
        except Exception as e:
            print(f"Erro ao carregar dados do médico: {e}")
            messages.warning(request, 'Perfil de médico não configurado. Entre em contato com o administrador.')
            context.update({
                'total_pacientes_medico': 0,
                'consultas_hoje_medico': 0,
                'proximas_consultas_medico': 0,
                'total_prontuarios_medico': 0,
                'consultas_medico_hoje': [],
                'ultimos_prontuarios_medico': []
            })
    
    else:  # recepcionista
        # Dados específicos para recepcionistas
        try:
            consultas_hoje = Consulta.objects.filter(data__date=hoje)
            proximas_consultas = Consulta.objects.filter(
                data__date=hoje,
                data__time__gte=timezone.now().time()
            ).order_by('data')[:5]
            
            context.update({
                'total_pacientes': Paciente.objects.count(),
                'consultas_hoje': consultas_hoje.count(),
                'consultas_pendentes': Consulta.objects.filter(status='PENDENTE').count(),
                'medicos_ativos': Medico.objects.filter(user__is_active=True).count(),
                'proximas_consultas': proximas_consultas,
            })
        except Exception as e:
            print(f"Erro ao carregar dados da recepcionista: {e}")
            context.update({
                'total_pacientes': 0,
                'consultas_hoje': 0,
                'consultas_pendentes': 0,
                'medicos_ativos': 0,
                'proximas_consultas': [],
            })
    
    return render(request, 'dashboard/dashboard.html', context)

# VIEWS DE PACIENTES (Admin e Recepcionista)
@recepcionista_or_admin_required
def pacientes(request):
    pacientes = Paciente.objects.annotate(
        ultima_consulta=Max('consulta__data')
    ).all()
    return render(request, 'pacientes/pacientes.html', {'pacientes': pacientes})

@recepcionista_or_admin_required
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
    
    return render(request, 'pacientes/cadastrar_paciente.html')

@all_authenticated_required
def visualizar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # Filtrar consultas baseado no tipo de usuário
    if request.user.user_type == 'medico':
        # Médicos só veem suas próprias consultas com o paciente
        try:
            medico = request.user.medico_profile
            consultas = Consulta.objects.filter(
                paciente=paciente, medico=medico
            ).select_related('medico').order_by('-data')
            prontuarios = Prontuario.objects.filter(
                consulta__paciente=paciente, consulta__medico=medico
            ).select_related('consulta', 'consulta__medico').order_by('-consulta__data')
        except:
            consultas = Consulta.objects.none()
            prontuarios = Prontuario.objects.none()
    else:
        # Admin e recepcionista veem todas as consultas
        consultas = Consulta.objects.filter(
            paciente=paciente
        ).select_related('medico').order_by('-data')
        prontuarios = Prontuario.objects.filter(
            consulta__paciente=paciente
        ).select_related('consulta', 'consulta__medico').order_by('-consulta__data')
    
    return render(request, 'pacientes/visualizar_paciente.html', {
        'paciente': paciente,
        'consultas': consultas,
        'prontuarios': prontuarios
    })

@recepcionista_or_admin_required
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
    
    return render(request, 'pacientes/editar_paciente.html', {'paciente': paciente})

# VIEWS DE CONSULTAS
@all_authenticated_required
def consultas(request):
    if request.user.user_type == 'medico':
        # Médicos só veem suas próprias consultas
        try:
            medico = request.user.medico_profile
            consultas = Consulta.objects.filter(medico=medico).select_related(
                'paciente', 'medico', 'medico__especialidade'
            ).order_by('data')
        except:
            consultas = Consulta.objects.none()
            messages.warning(request, 'Perfil de médico não configurado.')
    else:
        # Admin e recepcionista veem todas as consultas
        consultas = Consulta.objects.select_related(
            'paciente', 'medico', 'medico__especialidade'
        ).order_by('data')
    
    return render(request, 'consultas/consultas.html', {'consultas': consultas})

@recepcionista_or_admin_required
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
    return render(request, 'consultas/cadastrar_consulta.html', {
        'pacientes': pacientes,
        'medicos': medicos
    })

@all_authenticated_required
def visualizar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta.objects.select_related(
        'paciente', 'medico', 'medico__especialidade'
    ), id=consulta_id)
    
    # Verificar se o médico pode ver esta consulta
    if request.user.user_type == 'medico':
        try:
            if consulta.medico != request.user.medico_profile:
                messages.error(request, 'Você não tem permissão para ver esta consulta.')
                return redirect('consultas')
        except:
            messages.error(request, 'Perfil de médico não configurado.')
            return redirect('consultas')
    
    return render(request, 'consultas/visualizar_consulta.html', {'consulta': consulta})

@all_authenticated_required
def editar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    # Verificar permissões
    if request.user.user_type == 'medico':
        try:
            if consulta.medico != request.user.medico_profile:
                messages.error(request, 'Você não tem permissão para editar esta consulta.')
                return redirect('consultas')
        except:
            messages.error(request, 'Perfil de médico não configurado.')
            return redirect('consultas')
    
    if request.method == 'POST':
        try:
            if request.user.user_type in ['admin', 'recepcionista']:
                # Admin e recepcionista podem alterar tudo
                consulta.paciente_id = request.POST.get('paciente')
                consulta.medico_id = request.POST.get('medico')
                consulta.data = request.POST.get('data')
                consulta.motivo = request.POST.get('motivo')
            
            # Todos podem alterar o status
            consulta.status = request.POST.get('status')
            consulta.save()
            
            messages.success(request, 'Consulta atualizada com sucesso!')
            return redirect('consultas')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar consulta: {str(e)}')
    
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.select_related('especialidade').all()
    return render(request, 'consultas/editar_consulta.html', {
        'consulta': consulta,
        'pacientes': pacientes,
        'medicos': medicos
    })

@all_authenticated_required
def cancelar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    # Verificar permissões para médicos
    if request.user.user_type == 'medico':
        try:
            if consulta.medico != request.user.medico_profile:
                messages.error(request, 'Você não tem permissão para cancelar esta consulta.')
                return redirect('consultas')
        except:
            messages.error(request, 'Perfil de médico não configurado.')
            return redirect('consultas')
    
    if request.method == 'POST':
        try:
            consulta.status = 'CANCELADA'
            consulta.save()
            messages.success(request, 'Consulta cancelada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao cancelar consulta: {str(e)}')
    
    return redirect('consultas')

@medico_or_admin_required
def finalizar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    # Verificar se o médico pode finalizar esta consulta
    if request.user.user_type == 'medico':
        try:
            if consulta.medico != request.user.medico_profile:
                messages.error(request, 'Você não tem permissão para finalizar esta consulta.')
                return redirect('consultas')
        except:
            messages.error(request, 'Perfil de médico não configurado.')
            return redirect('consultas')
    
    if request.method == 'POST':
        try:
            consulta.status = 'FINALIZADA'
            consulta.concluida = True
            consulta.save()
            messages.success(request, 'Consulta finalizada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao finalizar consulta: {str(e)}')
    
    return redirect('consultas')

# VIEWS DE PRONTUÁRIOS (Médicos e Admin)
@medico_or_admin_required
def prontuarios(request):
    search = request.GET.get('search', '')
    
    if request.user.user_type == 'medico':
        # Médicos só veem seus próprios prontuários
        try:
            medico = request.user.medico_profile
            prontuarios = Prontuario.objects.filter(consulta__medico=medico).select_related(
                'consulta__paciente', 'consulta__medico', 'consulta__medico__especialidade'
            )
        except:
            prontuarios = Prontuario.objects.none()
            messages.warning(request, 'Perfil de médico não configurado.')
    else:
        # Admin vê todos os prontuários
        prontuarios = Prontuario.objects.select_related(
            'consulta__paciente', 'consulta__medico', 'consulta__medico__especialidade'
        ).all()
    
    if search:
        prontuarios = prontuarios.filter(
            consulta__paciente__nome__icontains=search
        )
    
    prontuarios = prontuarios.order_by('-consulta__data')
    
    return render(request, 'prontuario/prontuarios.html', {
        'prontuarios': prontuarios
    })

@medico_or_admin_required
def cadastrar_prontuario(request):
    if request.method == 'POST':
        try:
            consulta_id = request.POST.get('consulta')
            diagnostico = request.POST.get('diagnostico')
            anotacoes = request.POST.get('anotacoes')
            prescricao = request.POST.get('prescricao')
            
            consulta = get_object_or_404(Consulta, id=consulta_id)
            
            # Verificar se o médico pode criar prontuário para esta consulta
            if request.user.user_type == 'medico':
                try:
                    if consulta.medico != request.user.medico_profile:
                        messages.error(request, 'Você não tem permissão para criar prontuário para esta consulta.')
                        return redirect('prontuarios')
                except:
                    messages.error(request, 'Perfil de médico não configurado.')
                    return redirect('prontuarios')
            
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
    
    # Filtrar consultas baseado no tipo de usuário
    if request.user.user_type == 'medico':
        try:
            medico = request.user.medico_profile
            consultas_sem_prontuario = Consulta.objects.filter(
                medico=medico,
                prontuario__isnull=True,
                status__in=['CONFIRMADA', 'FINALIZADA']
            ).select_related('paciente', 'medico', 'medico__especialidade')
        except:
            consultas_sem_prontuario = Consulta.objects.none()
    else:
        consultas_sem_prontuario = Consulta.objects.filter(
            prontuario__isnull=True,
            status__in=['CONFIRMADA', 'FINALIZADA']
        ).select_related('paciente', 'medico', 'medico__especialidade')
    
    return render(request, 'prontuario/cadastrar_prontuario.html', {
        'consultas': consultas_sem_prontuario
    })

@medico_or_admin_required
def editar_prontuario(request, prontuario_id):
    prontuario = get_object_or_404(Prontuario, id=prontuario_id)
    
    # Verificar se o médico pode editar este prontuário
    if request.user.user_type == 'medico':
        try:
            if prontuario.consulta.medico != request.user.medico_profile:
                messages.error(request, 'Você não tem permissão para editar este prontuário.')
                return redirect('prontuarios')
        except:
            messages.error(request, 'Perfil de médico não configurado.')
            return redirect('prontuarios')
    
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
    
    return render(request, 'prontuario/editar_prontuario.html', {
        'prontuario': prontuario
    })

@medico_or_admin_required
def imprimir_prontuario(request, prontuario_id):
    prontuario = get_object_or_404(Prontuario, id=prontuario_id)
    
    # Verificar se o médico pode imprimir este prontuário
    if request.user.user_type == 'medico':
        try:
            if prontuario.consulta.medico != request.user.medico_profile:
                messages.error(request, 'Você não tem permissão para imprimir este prontuário.')
                return redirect('prontuarios')
        except:
            messages.error(request, 'Perfil de médico não configurado.')
            return redirect('prontuarios')
    
    return render(request, 'prontuario/imprimir_prontuario.html', {
        'prontuario': prontuario
    })

@all_authenticated_required
def agenda(request):
    if request.user.user_type == 'medico':
        try:
            medico = request.user.medico_profile
            consultas = Consulta.objects.filter(medico=medico).select_related('paciente')
        except:
            consultas = Consulta.objects.none()
    else:
        consultas = Consulta.objects.select_related('paciente', 'medico')
    
    return render(request, 'agenda/agenda.html', {'consultas': consultas})