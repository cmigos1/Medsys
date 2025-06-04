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
    
    for paciente_data in pacientes_exemplo:
        Paciente.objects.get_or_create(
            cpf=paciente_data['cpf'],
            defaults=paciente_data
        )
    
    print("Dados iniciais criados com sucesso!")
    print("Usuários criados:")
    print("- Admin: admin / admin123")
    print("- Médico: drcarlos / medico123")
    print("- Recepcionista: maria / recep123")

if __name__ == '__main__':
    create_initial_data()