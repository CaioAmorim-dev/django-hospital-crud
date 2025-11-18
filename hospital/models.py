from django.db import models

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    contato = models.IntegerField()
    cpf = models.CharField(max_length=11)

    def __str__(self):
        return self.nome

class Medico(models.Model):
    nome = models.CharField(max_length=100)
    numero = models.IntegerField()
    crm = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=11)

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