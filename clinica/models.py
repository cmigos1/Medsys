from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Administrador'),
        ('medico', 'Médico'),
        ('recepcionista', 'Recepcionista'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='recepcionista')
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def is_admin(self):
        return self.user_type == 'admin' or self.is_superuser
    
    def is_medico(self):
        return self.user_type == 'medico'
    
    def is_recepcionista(self):
        return self.user_type == 'recepcionista'


class Especialidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medico_profile')
    nome = models.CharField(max_length=100)
    crm = models.CharField(max_length=20, unique=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nome} ({self.crm})"

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('ESPERA', 'Em Espera'),
        ('FINALIZADA', 'Finalizada'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField()
    motivo = models.TextField()
    concluida = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    
    # Métodos de verificação de status
    def pode_ser_confirmada(self):
        return self.status == 'PENDENTE'
    
    def pode_ser_cancelada(self):
        return self.status in ['PENDENTE', 'CONFIRMADA']
    
    def pode_ir_para_espera(self):
        return self.status == 'CONFIRMADA'
    
    def pode_ter_prontuario(self):
        return self.status == 'ESPERA'
    
    def pode_ser_finalizada(self):
        return self.status == 'ESPERA' and hasattr(self, 'prontuario')
    
    # Métodos alternativos com nomes em inglês (para compatibilidade)
    def can_confirm(self):
        return self.pode_ser_confirmada()
    
    def can_cancel(self):
        return self.pode_ser_cancelada()
    
    def can_go_to_espera(self):
        return self.pode_ir_para_espera()
    
    def can_have_prontuario(self):
        return self.pode_ter_prontuario()
    
    def can_finalize(self):
        return self.pode_ser_finalizada()
    
    # Métodos de verificação de status atual
    def is_pending(self):
        return self.status == 'PENDENTE'
    
    def is_confirmed(self):
        return self.status == 'CONFIRMADA'
    
    def is_waiting(self):
        return self.status == 'ESPERA'
    
    def is_finished(self):
        return self.status == 'FINALIZADA'
    
    def is_cancelled(self):
        return self.status == 'CANCELADA'

    def __str__(self):
        return f"{self.paciente.nome} - {self.medico.nome} - {self.data.strftime('%d/%m/%Y')}"

class Prontuario(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE)
    anotacoes = models.TextField()
    diagnostico = models.TextField()
    prescricao = models.TextField(blank=True)

    def __str__(self):
        return f"Prontuário - {self.consulta.paciente.nome} - {self.consulta.data.strftime('%d/%m/%Y')}"

class Receita(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE)
    medicamento = models.CharField(max_length=100)
    posologia = models.TextField()

    def __str__(self):
        return f"{self.medicamento} - {self.prontuario.consulta.paciente.nome}"
