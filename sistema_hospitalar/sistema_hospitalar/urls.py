from django.urls import path
from . import views

urlpatterns = [
    # Pacientes
    path('pacientes/', views.listar_pacientes, name='listar_pacientes'),
    path('pacientes/novo/', views.criar_paciente, name='criar_paciente'),
    path('pacientes/editar/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/excluir/<int:id>/', views.excluir_paciente, name='excluir_paciente'),

]