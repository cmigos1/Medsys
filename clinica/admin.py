from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Especialidade, Medico, Paciente, Consulta, Prontuario, Receita

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'telefone')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'telefone')
        }),
    )

@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'crm', 'especialidade', 'user')
    list_filter = ('especialidade',)
    search_fields = ('nome', 'crm', 'user__username')
    raw_id_fields = ('user',)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'data_nascimento')
    search_fields = ('nome', 'cpf', 'telefone')
    list_filter = ('data_nascimento',)

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'data', 'status', 'concluida')
    list_filter = ('status', 'concluida', 'data', 'medico__especialidade')
    search_fields = ('paciente__nome', 'medico__nome', 'motivo')
    raw_id_fields = ('paciente', 'medico')
    date_hierarchy = 'data'

@admin.register(Prontuario)
class ProntuarioAdmin(admin.ModelAdmin):
    list_display = ('get_paciente', 'get_medico', 'get_data_consulta', 'diagnostico')
    search_fields = ('consulta__paciente__nome', 'consulta__medico__nome', 'diagnostico')
    list_filter = ('consulta__data', 'consulta__medico__especialidade')
    raw_id_fields = ('consulta',)
    
    def get_paciente(self, obj):
        return obj.consulta.paciente.nome
    get_paciente.short_description = 'Paciente'
    
    def get_medico(self, obj):
        return obj.consulta.medico.nome
    get_medico.short_description = 'Médico'
    
    def get_data_consulta(self, obj):
        return obj.consulta.data.strftime('%d/%m/%Y')
    get_data_consulta.short_description = 'Data da Consulta'

@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('medicamento', 'get_paciente', 'get_medico')
    search_fields = ('medicamento', 'prontuario__consulta__paciente__nome')
    raw_id_fields = ('prontuario',)
    
    def get_paciente(self, obj):
        return obj.prontuario.consulta.paciente.nome
    get_paciente.short_description = 'Paciente'
    
    def get_medico(self, obj):
        return obj.prontuario.consulta.medico.nome
    get_medico.short_description = 'Médico'