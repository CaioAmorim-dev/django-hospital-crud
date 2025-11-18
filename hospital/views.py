from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Paciente, Medico, Consulta
from .forms import PacienteForm, MedicoForm, ConsultaForm


# HOME DO SISTEMA 

def home(request):
    return render(request, 'home.html')


# PACIENTE 

def home_paciente(request):
    termo = request.GET.get('q', '')

    pacientes = Paciente.objects.all()

    if termo:
        pacientes = pacientes.filter(
            Q(nome__icontains=termo) |
            Q(cpf__icontains=termo) |
            Q(telefone__icontains=termo)
        )

    return render(request, 'paciente/home_paciente.html', {
        'termo': termo,
        'pacientes': pacientes
    })


def criar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('paciente_home')
    else:
        form = PacienteForm()

    return render(request, 'paciente/criar_paciente.html', {'form': form})


def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('paciente_home')
    else:
        form = PacienteForm(instance=paciente)

    return render(request, 'paciente/editar_paciente.html', {
        'form': form,
        'paciente': paciente
    })


def excluir_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'POST':
        paciente.delete()
        return redirect('paciente_home')

    return render(request, 'paciente/excluir_paciente.html', {'paciente': paciente})


# MEDICO 

def medico_home(request):
    termo = request.GET.get('q', '')

    medicos = Medico.objects.all().order_by('nome')

    if termo:
        medicos = medicos.filter(
            Q(nome__icontains=termo) |
            Q(especialidade__icontains=termo) |
            Q(crm__icontains=termo)
        )

    return render(request, 'medico/home_medico.html', {
        'termo': termo,
        'medicos': medicos
    })


def criar_medico(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medico_home')
    else:
        form = MedicoForm()

    return render(request, 'medico/criar_medico.html', {'form': form})


def editar_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)

    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('medico_home')
    else:
        form = MedicoForm(instance=medico)

    return render(request, 'medico/editar_medico.html', {
        'form': form,
        'medico': medico
    })


def excluir_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)

    if request.method == 'POST':
        medico.delete()
        return redirect('medico_home')

    return render(request, 'medico/excluir_medico.html', {'medico': medico})


#CONSULTA

def consulta_home(request):
    termo = request.GET.get('q', '')

    consultas = Consulta.objects.all()

    if termo:
        consultas = consultas.filter(
            Q(motivo__icontains=termo) |
            Q(paciente__nome__icontains=termo) |
            Q(medico__nome__icontains=termo)
        )

    return render(request, 'consulta/home_consulta.html', {
        'termo': termo,
        'consultas': consultas
    })


def criar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consulta_home')
    else:
        form = ConsultaForm()

    return render(request, 'consulta/criar_consulta.html', {'form': form})


def editar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)

    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('consulta_home')
    else:
        form = ConsultaForm(instance=consulta)

    return render(request, 'consulta/editar_consulta.html', {'form': form})


def excluir_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)

    if request.method == 'POST':
        consulta.delete()
        return redirect('consulta_home')

    return render(request, 'consulta/excluir_consulta.html', {'consulta': consulta})
