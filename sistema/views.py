from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required

@login_required(login_url= '/auth/login')
def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    else:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        return redirect('/auth/login/')