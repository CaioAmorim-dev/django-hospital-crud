from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    contato = models.CharField(max_length=15)  
    cpf = models.CharField(max_length=11, default="00000000000")
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome

    @property
    def idade(self):
        """Calcula a idade do paciente com base na data de nascimento."""
        
        if self.data_nascimento:
            today = date.today()
            idade = today.year - self.data_nascimento.year
            if today.month < self.data_nascimento.month or (today.month == self.data_nascimento.month and today.day < self.data_nascimento.day):
                idade -= 1
            return idade
        return None  # Retorna None se a data de nascimento não estiver definida
    
class Medico(models.Model):
    ESPECIALIDADE_CHOICES = [
        ('oftalmologia', 'Oftalmologia'),
        ('cardiologia', 'Cardiologia'),
        ('dermatologia', 'Dermatologia'),
    ]
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(
        max_length=255, 
        choices=ESPECIALIDADE_CHOICES,
        default='Clínico Geral'
    )
    
    crm = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=11, default="00000000000")

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    STATUS_CHOICES = [
        ('AG', 'Agendada'),
        ('RE', 'Realizada'),
        ('CA', 'Cancelada'),
    ]

    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='consultas')
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE, related_name='consultas')
    data = models.DateTimeField(db_index=True)
    situacao = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AG')

    def __str__(self):
        return f"{self.paciente.nome} - {self.medico.nome} ({self.get_situacao_display()})"

    def clean(self):
        # Verifica se a data da consulta é no passado
        if self.data and self.data < timezone.now():
            raise ValidationError("A data da consulta não pode ser no passado.")

    
    