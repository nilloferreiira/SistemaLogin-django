from django.shortcuts import render, redirect, HttpResponse
from hashlib import sha256
from django.contrib import messages, auth
from .models import Users as User
from .models import Users
from django.contrib.messages import constants

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/sistema/home')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})
    
def valida_cadastro(request):
    #Dados pessoais
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    #Dados residenciais
    rua = request.POST.get('rua')
    numero = request.POST.get('numero')
    cep =request.POST.get('cep')


    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
        return redirect('/auth/cadastro/')
    if len(senha) < 6:
        messages.add_message(request, constants.ERROR, 'Senha menor que 6 digitos!')
        return redirect('/auth/cadastro/')
    
  

    if User.objects.filter(email = email).exists():
        messages.add_message(request, constants.ERROR, 'Email já cadastrado no sistema!')
        return redirect('/auth/cadastro/')
    
    #
    
    try:
        usuario = User.objects.create_user(username = nome, email = email, password = senha, rua = rua, numero = numero, cep = cep)
        usuario.save()

        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso!')
        return redirect('/auth/cadastro/')

    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema!')
        return redirect('/auth/cadastro/')

def login(request):
    if request.user.is_authenticated:
        return redirect('/sistema/home')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def valida_login(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')

    usuario = auth.authenticate(request, username = nome, password = senha)

    if not usuario:
        messages.add_message(request, constants.WARNING, 'Email ou senha incorretos')
        return redirect('/auth/login/')
   
    else:
        auth.login(request, usuario)
        return redirect('/sistema/home')

def sair(request):
    auth.logout(request)
    return redirect('/auth/login/')


