from django.shortcuts import render, get_object_or_404, redirect
from .models import Paciente
from .models import Medico
from .forms import MedicoForm

# Create your views here.
def home(request):
    return render(request,"s /home.html")

def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/listar.html', {'pacientes': pacientes})

def criar_pacientes(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        idade = request.POST['idade']
        contato = request.POST['contato']
        Paciente.objects.create(nome=nome, idade=idade, contato=contato)
        return redirect('listar_pacientes')
    return render(request, 'pacientes/criar.html')

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