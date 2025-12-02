from django.core.management.base import BaseCommand
from django.utils import timezone
from hospital.models import Paciente, Medico, Consulta
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Coloca dados de teste no banco'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Apaga tudo antes',
        )

    def handle(self, *args, **options):
        if options['clear']:
            print('Apagando tudo...')
            Consulta.objects.all().delete()
            Paciente.objects.all().delete()
            Medico.objects.all().delete()
            print('Pronto, tudo limpo!')

        print('\nPopulando o banco...\n')

        
        print('Criando pacientes...')
        pacientes = self.criar_pacientes()
        print(f'{len(pacientes)} pacientes criados!')

        
        print('Criando médicos...')
        medicos = self.criar_medicos()
        print(f'{len(medicos)} médicos criados!')

        
        print('Criando consultas...')
        consultas = self.criar_consultas(pacientes, medicos)
        print(f'{len(consultas)} consultas criadas!')

        print('\nPronto! Deu tudo certo!\n')
        self.mostrar_resumo()

    def criar_pacientes(self):
        
        nomes = [
            'João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa', 'Carlos Souza',
            'Julia Lima', 'Roberto Alves', 'Fernanda Rocha', 'Lucas Martins', 'Patricia Gomes',
            'Ricardo Mendes', 'Camila Rodrigues', 'Bruno Cardoso', 'Amanda Ribeiro', 'Felipe Araujo',
            'Larissa Barbosa', 'Gustavo Pereira', 'Beatriz Castro', 'Thiago Carvalho', 'Isabela Dias',
            'Rafael Santos', 'Gabriela Monteiro', 'Diego Nascimento', 'Leticia Freitas', 'Marcelo Pinto',
            'Renata Teixeira', 'Andre Moreira', 'Vanessa Almeida', 'Paulo Vieira', 'Carolina Duarte',
        ]

        pacientes = []
        cpf_base = 10000000000  
        tel_base = 11900000000  

        for i, nome in enumerate(nomes, 1):
            
            anos = random.randint(5, 85)
            dias = random.randint(0, 364)
            data_nasc = datetime.now().date() - timedelta(days=anos * 365 + dias)

            paciente = Paciente.objects.create(
                nome=nome,
                cpf=str(cpf_base + i),
                contato=str(tel_base + i),
                data_nascimento=data_nasc
            )
            pacientes.append(paciente)

        return pacientes

    def criar_medicos(self):
        
        medicos_lista = [
            ('Dr. Alberto Silva', 'cardiologia', 'CRM123456'),
            ('Dra. Beatriz Costa', 'cardiologia', 'CRM123457'),
            ('Dr. Carlos Mendes', 'dermatologia', 'CRM123458'),
            ('Dra. Diana Santos', 'dermatologia', 'CRM123459'),
            ('Dr. Eduardo Lima', 'oftalmologia', 'CRM123460'),
            ('Dra. Fabiana Rocha', 'oftalmologia', 'CRM123461'),
            ('Dr. Gabriel Souza', 'cardiologia', 'CRM123462'),
            ('Dra. Helena Ribeiro', 'dermatologia', 'CRM123463'),
            ('Dr. Igor Barbosa', 'oftalmologia', 'CRM123464'),
            ('Dra. Julia Martins', 'cardiologia', 'CRM123465'),
        ]

        medicos = []
        cpf_base = 20000000000  

        for i, (nome, especialidade, crm) in enumerate(medicos_lista, 1):
            medico = Medico.objects.create(
                nome=nome,
                especialidade=especialidade,
                crm=crm,
                cpf=str(cpf_base + i)
            )
            medicos.append(medico)

        return medicos

    def criar_consultas(self, pacientes, medicos):
        consultas = []
        agora = timezone.now()

        print('  - Criando consultas passadas...')
        for _ in range(50):
            dias_atras = random.randint(1, 60)
            hora = random.randint(8, 17)
            minuto = random.choice([0, 30])
            
            data = agora - timedelta(days=dias_atras)
            data = data.replace(hour=hora, minute=minuto, second=0, microsecond=0)
            
            consulta = Consulta.objects.create(
                paciente=random.choice(pacientes),
                medico=random.choice(medicos),
                data=data,
                situacao='RE' 
            )
            consultas.append(consulta)

        print('  - Criando consultas de hoje...')
        for _ in range(5):
            hora = random.randint(8, 17)
            minuto = random.choice([0, 30])
            
            data = agora.replace(hour=hora, minute=minuto, second=0, microsecond=0)
            
            consulta = Consulta.objects.create(
                paciente=random.choice(pacientes),
                medico=random.choice(medicos),
                data=data,
                situacao=random.choice(['AG', 'AG', 'RE']) 
            )
            consultas.append(consulta)

        print('  - Criando consultas futuras...')
        for _ in range(60):
            dias_frente = random.randint(1, 90)
            hora = random.randint(8, 17)
            minuto = random.choice([0, 30])
            
            data = agora + timedelta(days=dias_frente)
            data = data.replace(hour=hora, minute=minuto, second=0, microsecond=0)
            
            consulta = Consulta.objects.create(
                paciente=random.choice(pacientes),
                medico=random.choice(medicos),
                data=data,
                situacao='AG'  
            )
            consultas.append(consulta)

        print('  - Criando algumas canceladas...')
        for _ in range(10):
            dias = random.randint(-30, 30)
            hora = random.randint(8, 17)
            minuto = random.choice([0, 30])
            
            data = agora + timedelta(days=dias)
            data = data.replace(hour=hora, minute=minuto, second=0, microsecond=0)
            
            consulta = Consulta.objects.create(
                paciente=random.choice(pacientes),
                medico=random.choice(medicos),
                data=data,
                situacao='CA'  
            )
            consultas.append(consulta)

        print('  - Criando mais consultas deste mes...')
        primeiro_dia = agora.replace(day=1, hour=8, minute=0, second=0, microsecond=0)
        
        for _ in range(20):
            dia = random.randint(1, 28)
            hora = random.randint(8, 17)
            minuto = random.choice([0, 30])
            
            data = primeiro_dia + timedelta(days=dia-1)
            data = data.replace(hour=hora, minute=minuto)
            
            if data < agora:
                status = 'RE'
            else:
                status = 'AG'
            
            consulta = Consulta.objects.create(
                paciente=random.choice(pacientes),
                medico=random.choice(medicos),
                data=data,
                situacao=status
            )
            consultas.append(consulta)

        return consultas

    def mostrar_resumo(self):
        # Vou mostrar o que foi criado
        total_pac = Paciente.objects.count()
        total_med = Medico.objects.count()
        total_cons = Consulta.objects.count()

        agora = timezone.now()
        hoje = agora.date()
        
        cons_hoje = Consulta.objects.filter(data__date=hoje).count()
        cons_mes = Consulta.objects.filter(data__year=agora.year, data__month=agora.month).count()
        cons_agendadas = Consulta.objects.filter(situacao='AG').count()
        cons_realizadas = Consulta.objects.filter(situacao='RE').count()
        cons_canceladas = Consulta.objects.filter(situacao='CA').count()

        print('='*50)
        print('RESUMO DO QUE FOI CRIADO:')
        print('='*50)
        print(f'Pacientes: {total_pac}')
        print(f'Medicos: {total_med}')
        print(f'Consultas: {total_cons}')
        print('')
        print('Consultas:')
        print(f'  - Hoje: {cons_hoje}')
        print(f'  - Este mes: {cons_mes}')
        print(f'  - Agendadas: {cons_agendadas}')
        print(f'  - Realizadas: {cons_realizadas}')
        print(f'  - Canceladas: {cons_canceladas}')
        print('')
        print('Medicos por especialidade:')
        cardio = Medico.objects.filter(especialidade='cardiologia').count()
        dermato = Medico.objects.filter(especialidade='dermatologia').count()
        oftalmo = Medico.objects.filter(especialidade='oftalmologia').count()
        print(f'  - Cardiologia: {cardio}')
        print(f'  - Dermatologia: {dermato}')
        print(f'  - Oftalmologia: {oftalmo}')
        print('='*50)
        print('\nAgora e so rodar o servidor e ver o dash!')