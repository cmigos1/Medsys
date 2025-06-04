from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def user_type_required(allowed_types):
    """
    Decorator para verificar se o usuário tem o tipo correto
    allowed_types: lista de tipos permitidos ['admin', 'medico', 'recepcionista']
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if not hasattr(request.user, 'user_type'):
                messages.error(request, 'Acesso negado: perfil de usuário não configurado.')
                return redirect('login')
            
            if request.user.user_type not in allowed_types:
                messages.error(request, 'Acesso negado: você não tem permissão para acessar esta página.')
                return redirect('dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def admin_required(view_func):
    """Decorator para views que só admins podem acessar"""
    return user_type_required(['admin'])(view_func)

def medico_or_admin_required(view_func):
    """Decorator para views que médicos e admins podem acessar"""
    return user_type_required(['admin', 'medico'])(view_func)

def recepcionista_or_admin_required(view_func):
    """Decorator para views que recepcionistas e admins podem acessar"""
    return user_type_required(['admin', 'recepcionista'])(view_func)

def all_authenticated_required(view_func):
    """Decorator para views que todos os usuários autenticados podem acessar"""
    return user_type_required(['admin', 'medico', 'recepcionista'])(view_func)