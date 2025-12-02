from django import forms
from django.core.exceptions import ValidationError
from .models import Paciente, Medico, Consulta
import re
from datetime import date


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        
        fields = ["nome", "idade", "contato", "cpf", "data_nascimento"]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do paciente'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a idade do paciente'}),
            'contato': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Telefone ou e-mail'}),
            'cpf': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CPF do paciente'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Data de nascimento'}),
        }

    def clean_contato(self):
        contato = self.cleaned_data.get("contato")

        if not contato:
            raise ValidationError("Contato é obrigatório.")
        
        
        contato_limpo = re.sub(r'\D', '', str(contato))

        
        if not re.fullmatch(r'\d{8,15}', contato_limpo):
            raise ValidationError("Telefone inválido. Digite apenas números (8 a 15 dígitos).")

        
        if Paciente.objects.filter(contato=contato_limpo).exclude(id=self.instance.id).exists():
            raise ValidationError("Este telefone já está cadastrado para outro paciente.")

        return contato_limpo

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")

        if not cpf:
            raise ValidationError("Erro! Digite o CPF novamente!")

        cpf_digits = re.sub(r'\D', '', str(cpf))

        if len(cpf_digits) != 11:
            raise ValidationError("CPF inválido. Deve conter 11 dígitos.")
        
        if cpf_digits == cpf_digits[0] * 11:
            raise ValidationError("CPF inválido.")

        if Paciente.objects.filter(cpf=cpf_digits).exclude(id=self.instance.id).exists():
            raise ValidationError("Este CPF já está cadastrado.")

        return cpf_digits

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get("data_nascimento")

        if not data_nascimento:
            raise ValidationError("Data de nascimento é obrigatória.")

        if data_nascimento and data_nascimento > date.today():
            raise ValidationError("A data de nascimento não pode ser no futuro.")
        
        idade = date.today().year - data_nascimento.year
        if idade > 130:
            raise ValidationError("Idade acima do limite permitido (130 anos).")

        return data_nascimento




class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        
        fields = ['nome', 'especialidade', 'crm', 'cpf']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nome do médico'}),
            'especialidade': forms.Select(attrs={'class': 'form-select'}),
            'crm': forms.TextInput(attrs={'class': 'form-control','placeholder': 'CRM do médico'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite o CPF do médico'}),
        }

    def clean_crm(self):
        crm = self.cleaned_data.get("crm")

        if not crm:
            raise ValidationError("CRM é obrigatório.")

        
        if not re.fullmatch(r'[A-Za-z0-9]{4,20}', str(crm)):
            raise ValidationError("CRM inválido. Use somente letras e números (4 a 20 caracteres).")

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
    cpf_paciente = forms.CharField(
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF do paciente'}),
        label='CPF do Paciente'
    )
    cpf_medico = forms.CharField(
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF do médico'}),
        label='CPF do Médico'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['cpf_paciente'].initial = self.instance.paciente.cpf
            self.fields['cpf_medico'].initial = self.instance.medico.cpf

    class Meta:
        model = Consulta
        fields = ['data', 'situacao']
        widgets = {
            'data': forms.DateTimeInput(attrs={'class': 'form-control','type': 'datetime-local'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_cpf_paciente(self):
        cpf = self.cleaned_data.get('cpf_paciente')
        cpf_digits = re.sub(r'\D', '', str(cpf))
        
        if len(cpf_digits) != 11:
            raise ValidationError("CPF inválido. Deve conter 11 dígitos.")
        
        try:
            paciente = Paciente.objects.get(cpf=cpf_digits)
            self.cleaned_data['paciente'] = paciente
        except Paciente.DoesNotExist:
            raise ValidationError("Paciente com este CPF não encontrado. Cadastre o paciente primeiro.")
        
        return cpf_digits

    def clean_cpf_medico(self):
        cpf = self.cleaned_data.get('cpf_medico')
        cpf_digits = re.sub(r'\D', '', str(cpf))
        
        if len(cpf_digits) != 11:
            raise ValidationError("CPF inválido. Deve conter 11 dígitos.")
        
        try:
            medico = Medico.objects.get(cpf=cpf_digits)
            self.cleaned_data['medico'] = medico
        except Medico.DoesNotExist:
            raise ValidationError("Médico com este CPF não encontrado. Cadastre o médico primeiro.")
        
        return cpf_digits

    def clean_data(self):
        from django.utils import timezone

        data = self.cleaned_data.get("data")

        if not data:
            raise ValidationError("A data da consulta é obrigatória.")

        
        if not self.instance.pk and data < timezone.now():
            raise ValidationError("A data da consulta não pode ser no passado.")

        return data

    def save(self, commit=True):
        consulta = super().save(commit=False)
        consulta.paciente = self.cleaned_data['paciente']
        consulta.medico = self.cleaned_data['medico']
        if commit:
            consulta.save()
        return consulta
