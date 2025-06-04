from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clinica.models import User

class Command(BaseCommand):
    help = 'Configura o usuário admin'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Nome de usuário')
        parser.add_argument('--email', type=str, help='Email do usuário')
        parser.add_argument('--password', type=str, help='Senha do usuário')

    def handle(self, *args, **options):
        username = options.get('username') or 'admin'
        email = options.get('email') or 'admin@medsys.com'
        password = options.get('password') or 'admin123'

        try:
            # Verificar se o usuário já existe
            user = User.objects.get(username=username)
            self.stdout.write(f'Usuário {username} já existe. Atualizando...')
            
            # Atualizar usuário existente
            user.email = email
            user.user_type = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            if password:
                user.set_password(password)
            user.save()
            
        except User.DoesNotExist:
            # Criar novo usuário
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                user_type='admin'
            )
            self.stdout.write(f'Usuário admin {username} criado com sucesso!')

        self.stdout.write(
            self.style.SUCCESS(
                f'Admin configurado:\n'
                f'Username: {user.username}\n'
                f'Email: {user.email}\n'
                f'Tipo: {user.user_type}\n'
                f'Is superuser: {user.is_superuser}\n'
                f'Is staff: {user.is_staff}'
            )
        )