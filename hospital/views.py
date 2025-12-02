from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from .models import Paciente, Medico, Consulta
from .forms import PacienteForm, MedicoForm, ConsultaForm
from datetime import date


# HOME DO SISTEMA 

def home(request):
    hoje= timezone.now().date()
    agora = timezone.now()

    contexto = {
        "total_pacientes" : Paciente.objects.count(),
        "total_medicos" : Medico.objects.count(),
        "total_consultas" : Consulta.objects.count(),
        "consultas_hoje": Consulta.objects.filter(data__date=hoje).count(),
        "consulta_mes" : Consulta.objects.filter(data__year=agora.year, data__month=agora.month).count(),
        "proximas_consultas" : Consulta.objects.filter(data__gte=agora).order_by('data')[:5],
        }
    

    return render(request, 'home.html', contexto)


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
        nome = request.POST.get('nome')
        contato = request.POST.get('contato')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')

        # Validação da data de nascimento
        if data_nascimento:
            data_nascimento_obj = date.fromisoformat(data_nascimento)
            hoje = date.today()
            
            if data_nascimento_obj > hoje:
                messages.error(request, "A data de nascimento não pode ser no futuro!")
                return redirect('paciente_home')

        Paciente.objects.create(
            nome=nome,
            contato=contato,
            cpf=cpf,
            data_nascimento=data_nascimento
        )
        
        messages.success(request, "Paciente criado com sucesso!")
        return redirect('paciente_home')

    return redirect('paciente_home')


def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'POST':
        paciente.nome = request.POST.get('nome')
        paciente.contato = request.POST.get('contato')
        paciente.cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        
        # Validação da data de nascimento
        if data_nascimento:
            data_nascimento_obj = date.fromisoformat(data_nascimento)
            hoje = date.today()
            
            if data_nascimento_obj > hoje:
                messages.error(request, "A data de nascimento não pode ser no futuro!")
                return redirect('paciente_home')
            
            paciente.data_nascimento = data_nascimento
        
        paciente.save()
        messages.success(request, "Paciente atualizado com sucesso!")
        return redirect('paciente_home')

    return redirect('paciente_home')


def excluir_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'POST':
        paciente.delete()
        messages.success(request, "Paciente excluído com sucesso!")
        return redirect('paciente_home')

    return redirect('paciente_home')


# MEDICO 

def home_medico(request):
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
        nome = request.POST.get('nome')
        especialidade = request.POST.get('especialidade')
        crm = request.POST.get('crm')
        contato = request.POST.get('contato', '')
        cpf = request.POST.get('cpf')
        
        Medico.objects.create(
            nome=nome,
            especialidade=especialidade,
            crm=crm,
            cpf=cpf
        )
        messages.success(request, "Médico criado com sucesso!")
        return redirect('medico_home')

    return redirect('medico_home')


def editar_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)

    if request.method == 'POST':
        medico.nome = request.POST.get('nome')
        medico.especialidade = request.POST.get('especialidade')
        medico.crm = request.POST.get('crm')
        medico.cpf = request.POST.get('cpf')
        
        medico.save()
        messages.success(request, "Médico atualizado com sucesso!")
        return redirect('medico_home')

    return redirect('medico_home')


def excluir_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)

    if request.method == 'POST':
        medico.delete()
        messages.success(request, "Médico excluído com sucesso!")
        return redirect('medico_home')

    return redirect('medico_home')


#CONSULTA

def consulta_home(request):
    consultas = Consulta.objects.all()
    print("CONSULTAS ENCONTRADAS:", consultas)
    return render(request, 'consulta/home_consultas.html', {'consultas': consultas})

def criar_consulta(request):
    if request.method == "POST":
        cpf_paciente = request.POST.get("cpf_paciente")
        cpf_medico = request.POST.get("cpf_medico")
        data = request.POST.get("data")
        situacao = request.POST.get("situacao")

        paciente = get_object_or_404(Paciente, cpf=cpf_paciente)
        medico = get_object_or_404(Medico, cpf=cpf_medico)

        Consulta.objects.create(
            paciente=paciente,
            medico=medico,
            data=data,
            situacao=situacao
        )
        
        messages.success(request, "Consulta criada com sucesso!")
        return redirect("consulta_home")

    return redirect("consulta_home")



def editar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)

    if consulta.situacao == "CA":
        messages.error(request, "Consultas canceladas não podem ser editadas.")
        return redirect("consulta_home")

    if request.method == 'POST':
        cpf_paciente = request.POST.get("cpf_paciente")
        cpf_medico = request.POST.get("cpf_medico")
        data = request.POST.get("data")
        situacao = request.POST.get("situacao")
        
        if cpf_paciente:
            consulta.paciente = get_object_or_404(Paciente, cpf=cpf_paciente)
        if cpf_medico:
            consulta.medico = get_object_or_404(Medico, cpf=cpf_medico)
        if data:
            consulta.data = data
        if situacao:
            consulta.situacao = situacao
        
        consulta.save()
        messages.success(request, "Consulta atualizada com sucesso!")
        return redirect('consulta_home')

    return redirect('consulta_home')


def cancelar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)

    if request.method == "POST":
        consulta.situacao = "CA"
        consulta.save()
        messages.success(request, "Consulta cancelada com sucesso!")
        return redirect("consulta_home")

    return redirect("consulta_home")



