from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
# listings/views.py
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

from django.urls import reverse
from django.http import HttpResponseForbidden
from terrains.models import Terrain
from django.shortcuts import render
from django.contrib import messages
from django.core.exceptions import ValidationError
from terrains.TerrainForm import TerrainForm

from terrains.ReservationForm import ReservationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from terrains.form_modife import UserUpdateForm
from terrains.form_2_change_info import UserUpdateForm_n

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

            if user.is_active:  # Vérifier si l'utilisateur est actif
                auth_login(request, user)
                if user.is_superuser:
                    return redirect('dashbord')
                else:
                    return redirect('profile')
            else:
                messages.error(request, "Votre compte est désactivé.")
        else:
            messages.error(request, "Email ou mot de passe invalide.")
    return render(request, 'terrains/login.html')



@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm_n(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data.get('new_password1')
            if new_password:
                user.set_password(new_password)
            user.save()
            return redirect('profile')
    else:
        form = UserUpdateForm_n(instance=request.user)

    return render(request, 'terrains/profil.html', {'form': form})
def user_logout(request):
    logout(request)
    return redirect('index')




def dashbord(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Vous n'avez pas l'autorisation d'accéder à cette page.")
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
    if not request.user.is_superuser:
        return HttpResponseForbidden("Vous n'avez pas l'autorisation d'accéder à cette page.")

    if request.method == 'POST':
        form = TerrainForm(request.POST, request.FILES)
        if form.is_valid():
            # Récupérer l'utilisateur superutilisateur
            super_user = User.objects.filter(is_superuser=True).first()

            # Créer une nouvelle instance de Terrain en associant l'administrateur
            terrain = form.save(commit=False)
            terrain.administrateur = super_user
            terrain.save()


            return redirect('dashbord')  # Rediriger vers une vue appropriée après l'ajout
    else:
        form = TerrainForm()


    superusers = User.objects.filter(is_superuser=True)
    return render(request, 'terrains/Ajoute_terrain.html',
                  {'form': form, 'disponibilite_choices': Terrain._meta.get_field('disponibilite').choices,
                   'administrateurs': superusers})
@login_required
def affiche_reservation(request, terrain_id, tarif_horaire):

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user  # Associer l'utilisateur connecté
            reservation.etat = "PASSEE"
            reservation.terrain_id = terrain_id
            reservation.save()
            return redirect('players')  # Assurez-vous de remplacer par le nom correct de votre URL
    else:
        form = ReservationForm(initial={'terrain_id': terrain_id, 'tarif_horaire': tarif_horaire})

    context = {
        'form': form,
        'terrain_id': terrain_id,
        'montant_payer': tarif_horaire,
    }

    return render(request, 'terrains/reservation.html', context)
def modifier_terrain(request, terrain_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Vous n'avez pas l'autorisation d'accéder à cette page.")

    terrain = get_object_or_404(Terrain, pk=terrain_id)
    if request.method == 'POST':
        form = TerrainForm(request.POST, request.FILES, instance=terrain)
        if form.is_valid():
            form.save()
            return redirect('liste_terrains')
    else:
        form = TerrainForm(instance=terrain)

    return render(request, 'terrains/Modifier_terrain.html', {'form': form, 'terrain': terrain,
                                                              'disponibilite_choices': Terrain._meta.get_field(
                                                                  'disponibilite').choices})



def supprimer_terrain(request, terrain_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Vous n'avez pas l'autorisation d'accéder à cette page.")

    if request.method == 'POST':
        terrain = get_object_or_404(Terrain, pk=terrain_id)
        terrain.delete()
        messages.success(request, 'Terrain supprimé avec succès')
    return redirect('liste_terrains')


def modifier_utilisateur(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        old_password = request.POST.get('old_password')

        if form.is_valid():
            # Vérifier l'ancien mot de passe
            if authenticate(username=user.username, password=old_password):
                # Mettre à jour les informations utilisateur
                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']

                # Changer le mot de passe si un nouveau est fourni
                new_password1 = form.cleaned_data.get('new_password1')
                new_password2 = form.cleaned_data.get('new_password2')
                if new_password1:
                    if new_password1 == new_password2:
                        user.set_password(new_password1)
                    else:
                        messages.error(request, "Les nouveaux mots de passe ne correspondent pas.")
                        return redirect('modifier_utilisateur')

                user.save()

                # Mettre à jour la session pour éviter la déconnexion
                update_session_auth_hash(request, user)
                messages.success(request, 'Votre profil a été mis à jour avec succès!')

                # Redirection en fonction du statut de l'utilisateur
                if user.is_superuser:
                    return redirect('dashbord')
                else:
                    return redirect('profile')
            else:
                messages.error(request, 'Ancien mot de passe incorrect.')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'terrains/changer_info_user.html', {'form': form})

def modifier_utilisateur_normal(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm_n(request.POST, instance=user)
        old_password = request.POST.get('old_password')

        if form.is_valid():
            # Vérifier l'ancien mot de passe
            if authenticate(username=user.username, password=old_password):
                # Mettre à jour les informations utilisateur
                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']

                # Changer le mot de passe si un nouveau est fourni
                new_password1 = form.cleaned_data.get('new_password1')
                if new_password1:
                    user.set_password(new_password1)

                user.save()

                # Mettre à jour la session pour éviter la déconnexion
                update_session_auth_hash(request, user)
                messages.success(request, 'Votre profil a été mis à jour avec succès!')
                return redirect('profile')
            else:
                messages.error(request, 'Ancien mot de passe incorrect.')
    else:
        form = UserUpdateForm_n(instance=user)

    return render(request, 'terrains/changer_info_user.html', {'form': form})


def reserver(request):
    return render(request, 'terrains/reserver.html')
