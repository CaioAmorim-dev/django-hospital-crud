from django.shortcuts import render, get_object_or_404, redirect
from .models import Paciente
from .forms import PacienteForm
from .models import Medico
from .forms import MedicoForm
from .models import Consulta
from .forms import ConsultaForm

# Create your views here.
def home(request):
    return render(request,"s /home.html")

def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/listar_pacientes.html', {'pacientes': pacientes})

def criar_pacientes(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_paciente')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/cria_paciente.html', {"form": form})

def editar_pacientes(resquest, id):
    paciente = get_object_or_404(Paciente, id=id)
    if resquest.method == 'POST':
        paciente.nome = resquest.POST['nome']
        paciente.idade = resquest.POST['idade']
        paciente.contato = resquest.POST['contato']
        paciente.save()
        return redirect('listar_pacientes')
    return render(resquest, 'pacientes/editar.html', {'paciente': paciente})

def excluir_pacientes(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('listar_pacientes')
    return render(request, 'pacientes/excluir.html', {'paciente': paciente})

def listar_medico(request):
    medicos = Medico.objects.all().order_by('nome')
    return render(request, 'clinica/listar_medico.html', {'medicos': medicos})

def criar_medico(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_medico')
        
    else:
        form = MedicoForm()
    return render(request, 'clinica/criar_medico.html', {'form': form})

def editar_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('listar_medico')
        
    else:  
        form = MedicoForm(instance=medico)
    return render(request, 'clinica/editar_medico.html',{
        'form':form,
        'medico': medico
    })

def excluir_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    if request.method == 'POST':
        medico.delete()
        return redirect('lista_medico')
    
    return render(request, 'clinica/excluir_medico.html', {'medico': medico})

def listar_consultas(request):
    consultas = Consulta.objects.all()
    return render(request, 'consultas/listar_consultas.html', {'consultas': consultas})

def criar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_consultas')
    else:
        form = ConsultaForm()
    return render(request, 'consultas/criar.html', {'form': form})

def editar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('listar_consultas')
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'consultas/editar_consulta.html', {'form': form})

def excluir_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    if request.method == 'POST':
        consulta.delete()
        return redirect('listar_consultas')
    return render(request, 'consultas/excluir_consulta.html', {'consulta': consulta})
