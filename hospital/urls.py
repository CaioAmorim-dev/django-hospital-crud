from django.urls import path
from . import views

urlpatterns = [

    # Página inicial do sistema
    path('', views.home, name='home'),

    #PACIENTE 
    path('paciente/', views.home_paciente, name='paciente_home'),

    path('paciente/novo/', views.criar_paciente, name='criar_paciente'),
    path('paciente/editar/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('paciente/excluir/<int:id>/', views.excluir_paciente, name='excluir_paciente'),


    #MEDICO 
    path('medico/', views.home_medico, name='medico_home'),

    path('medico/novo/', views.criar_medico, name='criar_medico'),
    path('medico/editar/<int:medico_id>/', views.editar_medico, name='editar_medico'),
    path('medico/excluir/<int:medico_id>/', views.excluir_medico, name='excluir_medico'),


    #CONSULTA 
    path('consulta/', views.consulta_home, name='consulta_home'),

    path('consulta/novo/', views.criar_consulta, name='criar_consulta'),
    path('consulta/editar/<int:id>/', views.editar_consulta, name='editar_consulta'),
    path("consultas/cancelar/<int:id>/", views.cancelar_consulta, name="cancelar_consulta"),
]
