from rest_framework import serializers
from .models import Paciente, Medico, Consulta

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'

class ConsultaSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    medico = MedicoSerializer(read_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.all(), source='paciente', write_only=True
    )
    medico_id = serializers.PrimaryKeyRelatedField(
        queryset=Medico.objects.all(), source='medico', write_only=True
    )
    situacao_display = serializers.CharField(source='get_situacao_display', read_only=True)

    class Meta:
        model = Consulta
        fields = [
            'id',
            'paciente',
            'medico',
            'paciente_id',
            'medico_id',
            'data',
            'situacao',
            'situacao_display'
        ]
