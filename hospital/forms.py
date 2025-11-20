from django import forms
from django.core.exceptions import ValidationError
from .models import Paciente, Medico, Consulta
import re
from datetime import date


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        # PACIENTE TEM: nome, idade, contato, cpf, data_nascimento
        fields = ["nome", "contato", "cpf", "data_nascimento"]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do paciente'}),
            'contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone ou e-mail'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CPF do paciente'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Data de nascimento'}),
        }

    def clean_contato(self):
        contato = self.cleaned_data.get("contato")

        if not contato:
            raise ValidationError("Contato é obrigatório.")

        # só aceita dígitos, de 8 a 15
        if not re.fullmatch(r'\d{8,15}', str(contato)):
            raise ValidationError("Telefone inválido. Digite apenas números (8 a 15 dígitos).")

        # valida duplicidade de contato
        if Paciente.objects.filter(contato=contato).exclude(id=self.instance.id).exists():
            raise ValidationError("Este telefone já está cadastrado para outro paciente.")

        return contato

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")

        if not cpf:
            raise ValidationError("Erro! Digite o CPF novamente!")

        cpf_digits = re.sub(r'\D', '', str(cpf))

        if len(cpf_digits) != 11:
            raise ValidationError("CPF inválido. Deve conter 11 dígitos.")

        if Paciente.objects.filter(cpf=cpf_digits).exclude(id=self.instance.id).exists():
            raise ValidationError("Este CPF já está cadastrado.")

        return cpf_digits

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get("data_nascimento")

        if data_nascimento and data_nascimento > date.today():
            raise ValidationError("A data de nascimento não pode ser no futuro.")

        return data_nascimento




class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        # MODELO TEM: nome, especialidade, crm, cpf
        fields = ['nome', 'especialidade', 'crm', 'cpf']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do médico'
            }),
            'especialidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especialidade'
            }),
            'crm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CRM do médico'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o CPF do médico'
            }),
        }

    def clean_crm(self):
        crm = self.cleaned_data.get("crm")

        if not crm:
            raise ValidationError("CRM é obrigatório.")

        # exemplo simples: só dígitos e letras, mínimo 4 caracteres
        if not re.fullmatch(r'[A-Za-z0-9]{4,20}', str(crm)):
            raise ValidationError("CRM inválido. Use de 4 a 20 caracteres, letras e números.")

        if Medico.objects.filter(crm=crm).exclude(id=self.instance.id).exists():
            raise ValidationError("Este CRM já está cadastrado para outro médico.")

        return crm

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")

        if not cpf:
            raise ValidationError("CPF é obrigatório.")

        cpf_digits = re.sub(r'\D', '', str(cpf))

        if len(cpf_digits) != 11:
            raise ValidationError("CPF inválido. Deve conter 11 dígitos.")

        if Medico.objects.filter(cpf=cpf_digits).exclude(id=self.instance.id).exists():
            raise ValidationError("Este CPF já está cadastrado para outro médico.")

        return cpf_digits


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'data', 'situacao']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'medico': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_data(self):
        from django.utils import timezone

        data = self.cleaned_data.get("data")

        if data and data < timezone.now():
            raise ValidationError("A data da consulta não pode ser no passado.")

        return data
