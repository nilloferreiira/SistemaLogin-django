from django.shortcuts import render, HttpResponse, redirect

def home(request):
    if request.session.get('logado'):
        return render(request, 'home.html')
    else:
        return redirect('/auth/login?status=7')