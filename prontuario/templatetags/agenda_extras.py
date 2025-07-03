from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """Permite acesso a chaves de dicionário no template"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, {})
    return {}

@register.filter
def get_consultas(agenda_dia):
    """Retorna as consultas de um dia específico"""
    if isinstance(agenda_dia, dict) and 'consultas' in agenda_dia:
        return agenda_dia['consultas']
    return []

@register.filter
def get_item(dictionary, key):
    """Filtro alternativo para acessar itens de dicionário"""
    try:
        return dictionary[key]
    except (KeyError, TypeError):
        return None

@register.simple_tag
def get_consultas_horario_dia(agenda, horario, dia):
    """Tag para obter consultas de um horário e dia específicos"""
    try:
        return agenda[horario][dia]['consultas']
    except (KeyError, TypeError):
        return []