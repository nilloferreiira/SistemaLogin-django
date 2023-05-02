from django.shortcuts import render, redirect, HttpResponse
from .models import Usuario
from hashlib import sha256
from django.contrib import messages
from django.contrib.messages import constants

def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})
    
def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    """
    status = 0 // sucesso
    status = 1 // campo de nome ou email incompletos
    stauts = 2 // senha mt fraca
    status = 3 // usuário já cadastrado no sistema
    status = 4 // erro interno do sistema
    """

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
        return redirect('/auth/cadastro/')
    if len(senha) < 6:
        messages.add_message(request, constants.ERROR, 'Senha menor que 6 digitos!')
        return redirect('/auth/cadastro/')
    
  

    usuarios = Usuario.objects.filter(email = email)
    if len(usuarios) != 0:
        messages.add_message(request, constants.ERROR, 'Email já cadastrado no sistema!')
        return redirect('/auth/cadastro/')
    
    try:
        senha = sha256(senha.encode()).hexdigest()

        usuario = Usuario(nome = nome, email = email, senha = senha)
        usuario.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso!')
        return redirect('/auth/cadastro/')

    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema!')
        return redirect('/auth/cadastro/')

def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha = sha256(senha.encode()).hexdigest()
    """
    status = 0 // sucesso
    status = 5 // Email ou senha incorretos
    status = 6 // Erro interno do sistema
    """

    usuarios = Usuario.objects.filter(email = email).filter(senha = senha)

    if len(usuarios) == 1:
        request.session['logado'] = True
        request.session['usuario_id'] = usuarios[0].id
        return redirect('/sistema/home')
   
    elif len(usuarios) == 0:
        messages.add_message(request, constants.WARNING, 'Email ou senha incorretos')
        return redirect('/auth/login/')
    
def sair(request):
    request.session.flush()
    return redirect('/auth/login/')

def login(request):
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

