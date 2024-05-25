from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponseForbidden
from terrains.models import Terrain, Reservation
from django.shortcuts import render
from django.contrib import messages
from terrains.TerrainForm import TerrainForm
from django.contrib.auth import update_session_auth_hash
from terrains.form_modife import UserUpdateForm
from terrains.form_2_change_info import UserUpdateForm_n
from django.core.paginator import Paginator
import io
from django.http import FileResponse, HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from .models import Facture
from django.urls import reverse

def index(request):
    terrains_list = Terrain.objects.all()
    return render(request, 'terrains/index.html', {'terrains_list': terrains_list})

def players(request):
    terrains_list = Terrain.objects.all()
    paginator = Paginator(terrains_list, 4)  # Affiche 5 terrains par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'terrains/players.html',
                  {'page_obj': page_obj, 'terrains_list': terrains_list})
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

    user = request.user
    reservations = Reservation.objects.filter(user=user).order_by('date_time')

    return render(request, 'terrains/profil.html', {'form': form, 'reservations': reservations})

def user_logout(request):
    logout(request)
    return redirect('index')
def blog(request):
    return render(request, 'terrains/blog.html')

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
    user = request.user  # Associer l'utilisateur connecté
    terrain = Terrain.objects.get(id=terrain_id)
    reservations = Reservation.objects.filter(terrain_id=terrain_id)
    # Créer une liste des dates réservées
    dates_reservees = [reservation.date_time for reservation in reservations]

    return render(request, 'terrains/reservation.html', {'terrain': terrain, 'tarif_horaire': tarif_horaire, 'user':user, 'dates_reservees': dates_reservees})


def envoyer_reservation(request):
    if request.method == 'POST':
        date_time_str = request.POST.get('date_time')  # Format: 2024-06-05T14:00
        terrain_id = request.POST.get('terrain_id')
        # Convertir la date_time de la requête en objet datetime naive
        date_time_format = "%Y-%m-%dT%H:%M"
        naive_date_time = datetime.strptime(date_time_str, date_time_format)
        # Convertir la date naive en date aware en utilisant le fuseau horaire actuel
        aware_date_time = timezone.make_aware(naive_date_time, timezone.get_current_timezone())
        # Récupérer les réservations pour le terrain donné
        reservations = Reservation.objects.filter(terrain_id=terrain_id)
        montant_payer = request.POST.get('montant_payer')
        for reservation in reservations:
            reservation_date_time = reservation.date_time
            # Assurez-vous que la date_time de la réservation est également aware
            if timezone.is_naive(reservation_date_time):
                reservation_date_time = timezone.make_aware(reservation_date_time, timezone.get_current_timezone())
            # Comparaison des deux objets datetime aware
            if reservation_date_time == aware_date_time:
                return render(request, 'terrains/reservation_modal.html', {'date_time': aware_date_time, 'terrain_id':terrain_id, 'tarif_horaire':montant_payer})
        terrain = Terrain.objects.get(id=terrain_id)
        etat = "PASSEE"
        reservation = Reservation(
            terrain_id=terrain,
            montant_payer=montant_payer,
            user=request.user,
            etat=etat,
            date_time=aware_date_time
        )
        reservation.save()
        return redirect('fact', reservation_id=reservation.id)
def fact(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    montant_payer = reservation.montant_payer
    fact = Facture.objects.create(
        reservations=reservation,
        montant=montant_payer,
        methode_paiement='Virement bancaire',
        date=datetime.now()  # Utiliser la date actuelle
    )
    facture_id = fact.id
    return redirect('generate_pdf', facture_id=facture_id)
def generate_pdf(request, facture_id):
    # Récupérer la facture à partir de l'ID
    try:
        facture = Facture.objects.get(id=facture_id)
        reservation = facture.reservations
        terrain = reservation.terrain_id
        user = reservation.user
    except Facture.DoesNotExist:
        return HttpResponse("Facture non trouvée", status=404)

    # Créer un buffer pour le PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Styles de texte
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    subtitle_style = styles['Heading2']

    # Contenu du PDF
    elements = []
    # Informations de l'utilisateur
    user_info = [
        Paragraph(f"<b>Nom:</b> {user.first_name} {user.last_name}", normal_style),
        Paragraph(f"<b>Email:</b> {user.email}", normal_style),
    ]

    elements += user_info
    elements.append(Spacer(1, 1 * cm))

    # Titre de la facture
    elements.append(Paragraph("Facture", title_style))
    elements.append(Spacer(1, 0.5 * cm))
    # Ajouter une image du terrain si elle existe
    if terrain.image:
        image_path = terrain.image.path
        elements.append(Image(image_path, width=10 * cm, height=5 * cm))
        elements.append(Spacer(1, 1 * cm))



    # Informations sur la facture
    facture_info = [
        Paragraph(f"<b>Facture ID:</b> {facture.id}", normal_style),
        Paragraph(f"<b>Date:</b> {facture.date.strftime('%d/%m/%Y')}", normal_style),
        Paragraph(f"<b>Montant:</b> {facture.montant} DH", normal_style),
        Paragraph(f"<b>Méthode de paiement:</b> {facture.methode_paiement}", normal_style),
    ]

    elements += facture_info
    elements.append(Spacer(1, 1 * cm))

    # Informations sur la réservation
    reservation_info = [
        ["Réservation ID:", reservation.id],
        ["Date et Heure:", reservation.date_time.strftime('%d/%m/%Y %H:%M')],
        ["Montant payé:", f"{reservation.montant_payer} DH"],
        ["État:", reservation.etat],
    ]

    reservation_table = Table(reservation_info, colWidths=[5 * cm, 10 * cm])
    reservation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(reservation_table)
    elements.append(Spacer(1, 1 * cm))

    # Informations sur le terrain
    terrain_info = [
        ["Terrain:", terrain.nom],
        ["Adresse:", terrain.adresse],
        ["Tarif horaire:", f"{terrain.tarif_horaire} DH"],
        ["Disponibilité:", terrain.disponibilite],
        ["Capacité de joueurs:", terrain.capacite_joueur]
    ]

    terrain_table = Table(terrain_info, colWidths=[5 * cm, 10 * cm])
    terrain_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(terrain_table)
    elements.append(Spacer(1, 1 * cm))

    # Finaliser le PDF
    doc.build(elements)

    # Revenir au début du buffer
    buffer.seek(0)

    # Envoyer le PDF en réponse
    return FileResponse(buffer, as_attachment=True, filename=f'facture_{facture.id}.pdf')

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


def reserver(request, terrain_id, tarif_horaire):
    return render(request, 'terrains/reserver.html', terrain_id, tarif_horaire)
@login_required
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.delete()
    return redirect(reverse('profile') + '?deleted=1')
    #return HttpResponse('Bien annulé')

def liste_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'terrains/liste_reservations.html', {'reservations': reservations})


def contact(request):
    return render(request, 'terrains/contact.html')

