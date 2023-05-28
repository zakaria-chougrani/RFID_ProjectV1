from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import CreerUtilisateur


def inscriptionPage(request):
    form = CreerUtilisateur()
    if request.method == 'POST':
        form = CreerUtilisateur(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.info(request, 'Votre compte a été créé avec succès: ' + user + " Veuillez s'identifier SVP")
            return redirect('acces')
    context = {'form': form}
    return render(request, 'compte/inscription.html', context)


def accesPage(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, "Compte Introuvable!!! Veuillez ressayer")
    return render(request, 'compte/acces.html', context)

def logoutPage(request):
    logout(request)
    return redirect('acces')

