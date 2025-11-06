from django import forms 
from .models import Paciente, Medico, Consulta

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["nome","idade", "contato", "situacao"]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do paciente'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Idade'}),
            'contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone ou e-mail'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
            }
            

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'numero']


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'data', 'situacao']