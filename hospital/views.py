from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib import messages
from .models import Paciente, Medico, Consulta
from .forms import PacienteForm, MedicoForm, ConsultaForm
from datetime import date


# HOME DO SISTEMA 

def home(request):
    hoje = timezone.now().date()
    agora = timezone.now()

    # Estatísticas gerais
    total_pacientes = Paciente.objects.count()
    total_medicos = Medico.objects.count()
    total_consultas = Consulta.objects.count()
    
    # Consultas por período
    consultas_hoje = Consulta.objects.filter(data__date=hoje).count()
    consulta_mes = Consulta.objects.filter(data__year=agora.year, data__month=agora.month).count()
    
    # Consultas por status
    consultas_agendadas = Consulta.objects.filter(situacao='AG').count()
    consultas_realizadas = Consulta.objects.filter(situacao='RE').count()
    
    # Próximas consultas (apenas agendadas e futuras)
    proximas_consultas = Consulta.objects.filter(
        data__gte=agora,
        situacao='AG'
    ).order_by('data')[:5]
    
    # Médicos por especialidade
    medicos_por_especialidade = Medico.objects.values('especialidade').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Adiciona o display name para cada especialidade
    for item in medicos_por_especialidade:
        especialidade_dict = dict(Medico.ESPECIALIDADE_CHOICES)
        item['especialidade__display'] = especialidade_dict.get(item['especialidade'], item['especialidade'])

    contexto = {
        "total_pacientes": total_pacientes,
        "total_medicos": total_medicos,
        "total_consultas": total_consultas,
        "consultas_hoje": consultas_hoje,
        "consulta_mes": consulta_mes,
        "consultas_agendadas": consultas_agendadas,
        "consultas_realizadas": consultas_realizadas,
        "proximas_consultas": proximas_consultas,
        "medicos_por_especialidade": medicos_por_especialidade,
        "data_atual": agora,
    }

    return render(request, 'home.html', contexto)


def home_paciente(request):
    termo = request.GET.get('q', '')
    data_nascimento_inicio = request.GET.get('data_nascimento_inicio', '')
    data_nascimento_fim = request.GET.get('data_nascimento_fim', '')
    contato = request.GET.get('contato', '')

    pacientes = Paciente.objects.all()

    if termo:
        pacientes = pacientes.filter(
            Q(nome__icontains=termo) |
            Q(cpf__icontains=termo) |
            Q(contato__icontains=termo)
        )

    if data_nascimento_inicio:
        pacientes = pacientes.filter(data_nascimento__gte=data_nascimento_inicio)
    if data_nascimento_fim:
        pacientes = pacientes.filter(data_nascimento__lte=data_nascimento_fim)

    if contato:
        pacientes = pacientes.filter(contato__icontains=contato)

    return render(request, 'paciente/home_paciente.html', {
        'termo': termo,
        'data_nascimento_inicio': data_nascimento_inicio,
        'data_nascimento_fim': data_nascimento_fim,
        'contato': contato,
        'pacientes': pacientes
    })


def criar_paciente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        contato = request.POST.get('contato')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')

        # Validar se o CPF já existe para paciente
        if Paciente.objects.filter(cpf=cpf).exists():
            messages.error(request, f"Já existe um paciente cadastrado com o CPF {cpf}. Por favor, utilize um CPF diferente.")
            return redirect('paciente_home')
        
        # Validar se o CPF já existe para médico (validação cross-table)
        if Medico.objects.filter(cpf=cpf).exists():
            messages.error(request, f"Este CPF ({cpf}) já está associado a um médico. Por favor, utilize um CPF diferente.")
            return redirect('paciente_home')

        # Validação da data de nascimento
        if data_nascimento:
            data_nascimento_obj = date.fromisoformat(data_nascimento)
            hoje = date.today()
            
            if data_nascimento_obj > hoje:
                messages.error(request, "A data de nascimento não pode ser no futuro!")
                return redirect('paciente_home')

        try:
            Paciente.objects.create(
                nome=nome,
                contato=contato,
                cpf=cpf,
                data_nascimento=data_nascimento
            )
            messages.success(request, "Paciente criado com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao criar paciente: {str(e)}")

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
        cpf = request.POST.get('cpf')

        # Validar se o CRM já existe
        if Medico.objects.filter(crm=crm).exists():
            messages.error(request, f"Já existe um médico cadastrado com o CRM {crm}. Por favor, utilize um CRM diferente.")
            return redirect('medico_home')

        # Validar se o CPF já existe para médico
        if Medico.objects.filter(cpf=cpf).exists():
            messages.error(request, f"Já existe um médico cadastrado com o CPF {cpf}. Por favor, utilize um CPF diferente.")
            return redirect('medico_home')
        
        # Validar se o CPF já existe para paciente (validação cross-table)
        if Paciente.objects.filter(cpf=cpf).exists():
            messages.error(request, f"Este CPF ({cpf}) já está associado a um paciente. Por favor, utilize um CPF diferente.")
            return redirect('medico_home')

        try:
            Medico.objects.create(
                nome=nome,
                especialidade=especialidade,
                crm=crm,
                cpf=cpf
            )
            messages.success(request, "Médico criado com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao criar médico: {str(e)}")

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

        try:
            paciente = get_object_or_404(Paciente, cpf=cpf_paciente)
            medico = get_object_or_404(Medico, cpf=cpf_medico)

            # Converter data string para datetime
            from datetime import datetime, timedelta
            data_datetime = datetime.fromisoformat(data)

            # Verificar conflito de horário: 20 minutos antes e depois
            intervalo_minimo = timedelta(minutes=20)
            
            consultas_conflito = Consulta.objects.filter(
                medico=medico,
                situacao__in=['AG', 'RE']  # Verificar apenas agendadas e realizadas
            ).filter(
                data__gte=data_datetime - intervalo_minimo,
                data__lte=data_datetime + intervalo_minimo
            ).exclude(id=None)  # Excluir consulta atual se estiver editando

            if consultas_conflito.exists():
                consulta_proxima = consultas_conflito.first()
                messages.error(
                    request, 
                    f"Conflito de horário! O médico {medico.nome} já possui uma consulta agendada próxima a este horário. "
                    f"Última consulta: {consulta_proxima.data.strftime('%d/%m/%Y às %H:%M')}. "
                    f"Por favor, escolha um horário com pelo menos 20 minutos de intervalo."
                )
                return redirect("consulta_home")

            Consulta.objects.create(
                paciente=paciente,
                medico=medico,
                data=data_datetime,
                situacao=situacao
            )
            messages.success(request, "Consulta criada com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao criar consulta: {str(e)}")

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



