from django import forms 
from .models import Paciente, Medico, Consulta

class pacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["nome","idade", "contato", "situacao"]

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'numero']


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'data', 'situacao']