from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
# listings/views.py
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

from terrains.models import Terrain
from .models import Client
from django.shortcuts import render
from django.contrib import messages

from terrains.TerrainForm import TerrainForm

from terrains.ReservationForm import ReservationForm
def index(request):
    return render(request, 'terrains/index.html')
#def hello(request):
 #   bands = Terrain.objects.all()
  #  return render(request, 'listings/hello.html',
   #               #{'first_band': bands[0]})
    #             {'bands': bands})


def players(request):
    terrains = Terrain.objects.all()
    return render(request, 'terrains/players.html',
                  {'terrains': terrains})
# Dans views.py


def terrain_details(request, terrain_id):
    terrain = get_object_or_404(Terrain, pk=terrain_id)
    return render(request, 'terrains/terrain_details.html', {'terrain': terrain})

def register(request):
    if request.method == 'POST':

        last_name = request.POST.get('name')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')


        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name,
                                        last_name=last_name)


        return redirect('index')


    return render(request, 'terrains/register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_superuser:
                return redirect('dashbord')
            else:
                auth_login(request, user)
                return redirect('profile')
        else:
            messages.error(request, "Invalid Email ou Mots de passe")
            return render(request, 'terrains/login.html', {})
    else:
        return render(request, 'terrains/login.html', {})



@login_required
def profile(request):
    user = request.user

    context = {
        'user': user,
    }

    return render(request, 'terrains/profil.html', context)

def user_logout(request):
    logout(request)
    return redirect('index')


def dashbord(request):
    return render(request, 'terrains/dashbord.html')
def liste_terrains(request):
    terrains = Terrain.objects.all()
    return render(request, 'terrains/page_aff_terrain.html', {'terrains': terrains})

def liste_utilisateurs(request):
    utilisateurs = User.objects.exclude(is_staff=True)
    context = {
        'utilisateurs': utilisateurs
    }
    return render(request, 'terrains/list_users.html', context)





def Ajout_terrain(request):
    if request.method == 'POST':
        form = TerrainForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashbord')  # Rediriger vers une vue appropriée après l'ajout
    else:
        form = TerrainForm()

    superusers = User.objects.filter(is_superuser=True)
    return render(request, 'terrains/Ajoute_terrain.html',
                  {'form': form, 'disponibilite_choices': Terrain._meta.get_field('disponibilite').choices,
                   'administrateurs': superusers})


def affiche_reservation(request, terrain_id, tarif_horaire):
    terrain = get_object_or_404(Terrain, id=terrain_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Assurez-vous de remplacer par le nom correct de votre URL
    else:
        form = ReservationForm(initial={'terrain_id': terrain.id, 'tarif_horaire': tarif_horaire})

    clients = Client.objects.all()
    terrains = Terrain.objects.all()
    context = {
        'form': form,
        'clients': clients,
        'terrains': terrains,
        'terrain': terrain,
        'tarif_horaire': tarif_horaire,
    }

    return render(request, 'terrains/reservation.html', context)