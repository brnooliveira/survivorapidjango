from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from core.models import Inventory
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import SurvivorSerializer
from rest_framework.exceptions import ValidationError

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


class SurvivorAPIView(APIView):
    serializer_class = SurvivorSerializer

    def get_object(self, pk):
        try:
            survivor = Survivor.objects.get(pk=pk)
            if survivor.is_infected:
                raise ValidationError('Survivor is infected')
            return survivor

        except Survivor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        return Survivor.objects.filter(is_infected=False)

    def get(self, request, pk=None):
        if pk:
            survivor = self.get_object(pk)
            serializer = self.serializer_class(survivor)
        else:
            survivors = self.get_queryset()
            serializer = self.serializer_class(survivors, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        survivor = self.get_object(pk)
        serializer = self.serializer_class(survivor, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        survivor = self.get_object(pk)
        survivor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InfectedSurvivorView(APIView):
    serializer_class = SurvivorSerializer

    def get(self, request):
        infected_survivors = Survivor.objects.filter(is_infected=True)
        serializer = self.serializer_class(infected_survivors, many=True)
        return Response(serializer.data)
