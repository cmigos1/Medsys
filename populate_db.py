import os
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prontuario.settings')
django.setup()

from clinica.models import User, Especialidade, Medico, Paciente
from django.contrib.auth.hashers import make_password

def create_initial_data():
    # Criar especialidades
    especialidades = [
        'Clínico Geral',
        'Cardiologia',
        'Dermatologia',
        'Pediatria',
        'Ginecologia',
        'Ortopedia'
    ]
    
    for esp_nome in especialidades:
        Especialidade.objects.get_or_create(nome=esp_nome)
    
    # Criar usuário admin
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@medsys.com',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'user_type': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'password': make_password('admin123')
        }
    )
    
    # Criar usuário médico
    medico_user, created = User.objects.get_or_create(
        username='drcarlos',
        defaults={
            'email': 'carlos@medsys.com',
            'first_name': 'Carlos',
            'last_name': 'Silva',
            'user_type': 'medico',
            'password': make_password('medico123')
        }
    )
    
    # Criar perfil do médico
    if created:
        cardiologia = Especialidade.objects.get(nome='Cardiologia')
        Medico.objects.get_or_create(
            user=medico_user,
            defaults={
                'nome': 'Dr. Carlos Silva',
                'crm': '12345-SP',
                'especialidade': cardiologia
            }
        )
    
    # Criar usuário recepcionista
    recep_user, created = User.objects.get_or_create(
        username='maria',
        defaults={
            'email': 'maria@medsys.com',
            'first_name': 'Maria',
            'last_name': 'Santos',
            'user_type': 'recepcionista',
            'password': make_password('recep123')
        }
    )
    
    # Criar alguns pacientes de exemplo
    pacientes_exemplo = [
        {
            'nome': 'João da Silva',
            'data_nascimento': '1980-05-15',
            'cpf': '123.456.789-00',
            'telefone': '(11) 99999-9999',
            'endereco': 'Rua A, 123, São Paulo - SP'
        },
        {
            'nome': 'Maria Oliveira',
            'data_nascimento': '1990-08-22',
            'cpf': '987.654.321-00',
            'telefone': '(11) 88888-8888',
            'endereco': 'Rua B, 456, São Paulo - SP'
        }
    ]

    pacientes_criados = []
    for paciente_data in pacientes_exemplo:
        paciente, created = Paciente.objects.get_or_create(
            cpf=paciente_data['cpf'],
            defaults=paciente_data
        )
        pacientes_criados.append(paciente)
    
    # Criar consultas de exemplo
    from clinica.models import Consulta
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    # Obter o médico criado
    try:
        medico = Medico.objects.get(user=medico_user)
        
        # Criar algumas consultas em diferentes status
        consultas_exemplo = [
            {
                'paciente': pacientes_criados[0],
                'medico': medico,
                'data': timezone.now() + timedelta(hours=1),
                'motivo': 'Consulta de rotina - Check-up',
                'status': 'PENDENTE'
            },
            {
                'paciente': pacientes_criados[1],
                'medico': medico,
                'data': timezone.now() + timedelta(hours=2),
                'motivo': 'Dor no peito - Emergência',
                'status': 'ESPERA'
            },
            {
                'paciente': pacientes_criados[0],
                'medico': medico,
                'data': timezone.now() + timedelta(days=1),
                'motivo': 'Retorno cardiologia',
                'status': 'CONFIRMADA'
            }
        ]
        
        for consulta_data in consultas_exemplo:
            Consulta.objects.get_or_create(
                paciente=consulta_data['paciente'],
                medico=consulta_data['medico'],
                data=consulta_data['data'],
                defaults={
                    'motivo': consulta_data['motivo'],
                    'status': consulta_data['status']
                }
            )
        
        print("Consultas de exemplo criadas!")
        
    except Exception as e:
        print(f"Erro ao criar consultas: {e}")

    print("Dados iniciais criados com sucesso!")
    print("Usuários criados:")
    print("- Admin: admin / admin123")
    print("- Médico: drcarlos / medico123")
    print("- Recepcionista: maria / recep123")

if __name__ == '__main__':
    create_initial_data()