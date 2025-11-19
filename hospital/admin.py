from django.contrib import admin
from .models import Paciente
from django import forms
from django.forms import DateInput

# FILTRO PACIENTE
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento']

    # Customiza o campo de data para exibir o formato DD/MM/AAAA
    data_nascimento = forms.DateField(
        widget=DateInput(attrs={
            'type': 'date',  # Isso garante que o navegador exiba o seletor de data
            'class': 'form-control',  # Estilo do campo
            'placeholder': 'DD/MM/AAAA'  # Placeholder para o formato
        })
    )

class PacienteAdmin(admin.ModelAdmin):
    form = PacienteForm
    list_display = ('nome', 'cpf', 'data_nascimento')  # Adiciona o campo de data de nascimento à lista
    search_fields = ('nome', 'cpf', )  # Permite pesquisar por nome, cpf e contato

    fieldsets = (
        (None, {
            'fields': ('nome', 'cpf', 'data_nascimento')  # Campos do formulário de cadastro
        }),
    )

# Registra o modelo Paciente com a customização
admin.site.register(Paciente, PacienteAdmin)
