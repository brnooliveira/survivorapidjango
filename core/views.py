from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from core.models import Inventory

Survivor = get_user_model()


def add_survivor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        password = request.POST.get('password')
        inventory = Inventory.objects.create()

        # Cria o usuário e o salva no banco de dados
        user = Survivor.objects.create_user(username=username,
                                            age=age,
                                            gender=gender,
                                            latitude=latitude,
                                            longitude=longitude,
                                            password=password,
                                            inventory=inventory)

        # Autentica o usuário recém-criado e faz login
        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect('/login/')  # redireciona para a página de login

    return render(request, 'registration/add_survivor.html')


@login_required
def profile(request):
    survivor = request.user
    print(survivor.id)  # Verifica se survivor possui atributo id
    survivors = Survivor.objects.exclude(
        id=survivor.id).prefetch_related('inventory')
    return render(request, 'registration/profile.html', {'survivor': survivor, 'survivors': survivors})
