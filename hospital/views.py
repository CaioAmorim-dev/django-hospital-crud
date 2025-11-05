from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"s /home.html")

def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/listar.html', {'pacientes': pacientes})