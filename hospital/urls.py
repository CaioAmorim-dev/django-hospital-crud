from django.urls import path
from . import views

urlpatterns = [
    # Pacientes
    path('', views.home, name='home'),
    path('pacientes/', views.listar_pacientes, name='listar_pacientes'),
    path('pacientes/novo/', views.criar_pacientes, name='criar_paciente'),
    path('pacientes/editar/<int:id>/', views.editar_pacientes, name='editar_paciente'),
    path('pacientes/excluir/<int:id>/', views.excluir_pacientes, name='excluir_paciente'),

    # Médicos
    path('medicos/', views.listar_medicos, name='listar_medicos'),
    path('medicos/novo/', views.criar_medico, name='criar_medico'),
    path('medicos/editar/<int:id>/', views.editar_medico, name='editar_medico'),
    path('medicos/excluir/<int:id>/', views.excluir_medico, name='excluir_medico'),

    # Consultas
    path('consultas/', views.listar_consultas, name='listar_consultas'),
    path('consultas/novo/', views.criar_consulta, name='criar_consulta'),
    path('consultas/editar/<int:id>/', views.editar_consulta, name='editar_consulta'),
    path('consultas/excluir/<int:id>/', views.excluir_consulta, name='excluir_consulta'),
]