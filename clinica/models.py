from django.db import models

# Create your models here.

class Especialidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Medico(models.Model):
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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')  # novo campo

    def __str__(self):
        return f"Consulta de {self.paciente.nome} com {self.medico.nome} em {self.data.strftime('%d/%m/%Y %H:%M')}"


class Prontuario(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE)
    anotacoes = models.TextField()
    diagnostico = models.TextField()
    prescricao = models.TextField(blank=True)

    def __str__(self):
        return f"Prontuário da consulta {self.consulta.id}"


class Receita(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE)
    medicamento = models.CharField(max_length=100)
    posologia = models.TextField()

    def __str__(self):
        return f"{self.medicamento} - {self.posologia}"
