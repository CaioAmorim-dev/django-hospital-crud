from django import forms 
from django.core.exceptions import ValidationError
from .models import Paciente, Medico, Consulta
import re

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["nome","idade", "contato", "CPF"]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do paciente'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Idade'}),
            'contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone ou e-mail'}),
            'CPF': forms.TextInputInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CPF do paciente'}),
            }
        
    def clean_idade(self):
        idade = self.cleaned_data. get("idade")

        if idade is None:
         raise ValidationError("Idade é obrigatória.")
        
        if idade < 0:
         raise ValidationError("A idade não pode ser negativa. Tente novamente!")
        return idade
    
    

    def clean_contato(self):
        contato = self.cleaned_data.get("contato")

        if not contato:
            raise ValidationError("Contato é obrigatório.")

        if not re.fullmatch(r'\d{8,15}', str(contato)):
            raise ValidationError("Telefone inválido. Digite apenas números (8 a 15 dígitos).")

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


            

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'numero']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do médico'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de registro'}),
            'CPF': forms.TextInputInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CPF do paciente'}),
        }

    def clean_numero(self):
        numero = self.cleaned_data.get("numero")

        if not numero:
            raise ValidationError("Número é obrigatório.")

        if not re.fullmatch(r'\d{8,15}', str(numero)):
            raise ValidationError("Número inválido. Digite apenas números (8 a 15 dígitos).")

        if Medico.objects.filter(numero=numero).exclude(id=self.instance.id).exists():
            raise ValidationError("Este número já está cadastrado para outro médico.")

        return numero

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




class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'data', 'situacao']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'medico': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_data(self):
        from datetime import datetime

        data = self.cleaned_data.get("data")

        if data and data < datetime.now():
            raise ValidationError("A data da consulta não pode ser no passado.")

        return data
