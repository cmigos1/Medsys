from django.contrib import admin
from .models import Especialidade, Medico, Paciente, Consulta, Prontuario, Receita

# Register your models here.

admin.site.register(Especialidade)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Consulta)
admin.site.register(Prontuario)
admin.site.register(Receita)
