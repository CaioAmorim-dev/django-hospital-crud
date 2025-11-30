from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from .models import Paciente, Medico, Consulta
from .models import Paciente, Medico, Consulta
from .forms import PacienteForm, MedicoForm, ConsultaForm


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
        idade = request.POST.get('idade')
        contato = request.POST.get('contato')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')

        Paciente.objects.create(
            nome=nome,
            contato=contato,
            cpf=cpf,
            data_nascimento=data_nascimento
        )

        return redirect('paciente_home')  # volta para a lista

    return redirect('paciente_home')


def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente atualizado com sucesso!")
            return redirect('paciente_home')
        else:
            messages.error(request, "Erro ao atualizar paciente. Verifique os dados.")
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
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico criado com sucesso!")
            return redirect('medico_home')
        else:
            messages.error(request, "Erro ao criar médico. Verifique os dados.")
            return redirect('medico_home')

    return redirect('medico_home')


def editar_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)

    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico atualizado com sucesso!")
            return redirect('medico_home')
        else:
            messages.error(request, "Erro ao atualizar médico. Verifique os dados.")
            return redirect('medico_home')
    else:
        form = MedicoForm(instance=medico)

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

        return redirect("consulta_home")

    return redirect("consulta_home")



def editar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)

    if consulta.situacao == "CA":
        messages.error(request, "Consultas canceladas não podem ser editadas.")
        return redirect("consulta_home")

    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "Consulta atualizada com sucesso!")
            return redirect('consulta_home')
        else:
            messages.error(request, "Erro ao atualizar consulta. Verifique os dados.")
            return redirect('consulta_home')

    return redirect('consulta_home')


def cancelar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)

    if request.method == "POST":
        consulta.situacao = "CA"  # Cancelada
        consulta.save()
        return redirect("consulta_home")

    return redirect("consulta_home")

# FILTRO PACIENTE

def home_paciente(request):
    termo = request.GET.get('q', '')  # Termo de pesquisa geral
    data_nascimento_inicio = request.GET.get('data_nascimento_inicio', '')
    data_nascimento_fim = request.GET.get('data_nascimento_fim', '')
    contato = request.GET.get('contato', '')

    # Inicia a consulta, buscando todos os pacientes
    pacientes = Paciente.objects.all()

    # Filtro por nome, CPF e telefone
    if termo:
        pacientes = pacientes.filter(
            Q(nome__icontains=termo) |
            Q(cpf__icontains=termo) |
            Q(contato__icontains=termo)
        )

    # Filtro por data de nascimento (intervalo)
    if data_nascimento_inicio:
        pacientes = pacientes.filter(data_nascimento__gte=data_nascimento_inicio)
    if data_nascimento_fim:
        pacientes = pacientes.filter(data_nascimento__lte=data_nascimento_fim)

    # Filtro por contato (telefone ou e-mail)
    if contato:
        pacientes = pacientes.filter(contato__icontains=contato)

    # Passando o filtro de termo e a lista de pacientes para o Template
    return render(request, 'paciente/home_paciente.html', {
        'termo': termo,
        'data_nascimento_inicio': data_nascimento_inicio,
        'data_nascimento_fim': data_nascimento_fim,
        'contato': contato,
        'pacientes': pacientes
    })



