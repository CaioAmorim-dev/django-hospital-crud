@@ -1,6 +1,6 @@
# 🏥 Sistema Hospitalar — Projeto de Introdução à Programação

## Introdução


Este projeto foi desenvolvido como parte da disciplina **Introdução à Programação** da Cesar School, com o objetivo de aplicar na prática os conceitos fundamentais de lógica de programação, orientação a objetos e desenvolvimento web utilizando o framework **Django**.

A proposta consiste em um **Sistema Hospitalar** que permite o gerenciamento básico de informações através de operações **CRUD (Create, Read, Update e Delete)**. O sistema possibilita o cadastro, visualização, edição e exclusão de dados de pacientes, médicos e consultas, buscando simular um ambiente de gestão hospitalar simples, porém funcional.

O projeto foi desenvolvido de forma colaborativa por uma equipe de seis integrantes, reforçando o aprendizado sobre trabalho em grupo, versionamento de código (Git/GitHub) e boas práticas de desenvolvimento em Python.


## Equipe

Allan Max de Jesus Rodrigues de Lima

Boniek Araújo dos Santos Júnior

Caio César Leandro Amorim

Miguel Victor Lussac Barboza

Vinícius Pessoa de Albuquerque

Wesley Yuri da Silva



## líider

Caio César Leandro Amorim

## Tema

Sistema hospitalar


### Orientações para rodar projeto

**Criar ambiente virtual**
```
python -m venv venv
```
**Acessar ambiente virutal**
```
venv\Scripts\activate
```
**instalar django**
```
pip install django
```
**Fazer migrations**
```
python manage.py makemigrations
```
**Aplicar migrations**
```
python manage.py migrate
```
**Rodar o servidor**
```
python manage.py runserver
```
**Acessar servidor no navegador**
```
👉 http://127.0.0.1:8000
```