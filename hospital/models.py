from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, date

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField(default=0)
    cpf = models.CharField(max_length=11, unique=True)
    contato = models.CharField(max_length=15)
    data_nascimento = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Se vier string, converte para date
        if isinstance(self.data_nascimento, str):
            self.data_nascimento = datetime.strptime(
                self.data_nascimento, "%Y-%m-%d"
            ).date()

        # Calcula idade
        hoje = date.today()
        self.idade = hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

        super().save(*args, **kwargs)


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
        if self.data and self.data < timezone.now():
            raise ValidationError("A data da consulta não pode ser no passado.")
