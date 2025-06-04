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
