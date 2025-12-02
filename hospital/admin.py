from django.contrib import admin
from .models import Paciente, Medico, Consulta
from django import forms
from django.forms import DateInput


class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'data_nascimento')
    search_fields = ('nome', 'cpf')
    list_filter = ('data_nascimento',)  
    fieldsets = (
        (None, {
            'fields': ('nome', 'cpf', 'data_nascimento')
        }),
    )


class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'especialidade', 'crm')
    search_fields = ('nome', 'cpf', 'especialidade', 'crm')
    list_filter = ('especialidade', 'crm')  # Filtro por especialidade e CRM
    fieldsets = (
        (None, {
            'fields': ('nome', 'cpf', 'especialidade', 'crm')
        }),
    )


class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'data', 'situacao')
    search_fields = ('paciente__nome', 'medico__nome')
    list_filter = ('data', 'paciente', 'medico', 'situacao')  # Filtro por data, paciente, médico e situação
    fieldsets = (
        (None, {
            'fields': ('paciente', 'medico', 'data', 'situacao')
        }),
    )


admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Consulta, ConsultaAdmin)
