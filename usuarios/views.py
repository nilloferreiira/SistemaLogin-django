from django.shortcuts import render, redirect, HttpResponse
from .models import Usuario
from hashlib import sha256

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
        return redirect('/auth/cadastro/?status=1')
    if len(senha) < 6:
        return redirect('/auth/cadastro/?status=2')
    
  

    usuarios = Usuario.objects.filter(email = email)
    if len(usuarios) != 0:
        return redirect('/auth/cadastro/?status=3')
    
    try:
        senha = sha256(senha.encode()).hexdigest()

        usuario = Usuario(nome = nome, email = email, senha = senha)
        usuario.save()
        return redirect('/auth/cadastro/?status=0')

    except:
        return redirect('/auth/cadastro/?status=4')

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
        return redirect('/sistema/home')
   
    elif len(usuarios) == 0:
        return redirect('/auth/login/?status=5')
    
def sair(request):
    request.session['logado'] = None
    return redirect('/auth/login/')
    
def login(request):
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

