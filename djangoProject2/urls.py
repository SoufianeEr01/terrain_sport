from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.conf.urls.static import static, settings
from terrains import views

urlpatterns = [
    path('dashbord/', views.dashbord, name='dashbord'),
    path('index/', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('reservation/<int:terrain_id>/<str:tarif_horaire>/', views.affiche_reservation, name='affiche_reservation'),
   # path('reservationf/', views.reservation_create, name='reservation_create'),
    path('profile/', views.profile, name='profile'),
    path('', views.index),
    path('players/', views.players, name='players'),
    path('admin/', admin.site.urls, name='admin'),
    path('logout/', views.user_logout, name='logout'),
    path('terrains/', views.liste_terrains, name='liste_terrains'),
    path('utilisateurs/', views.liste_utilisateurs, name='list_usr'),
    path('ajout_terrain/', views.Ajout_terrain, name='Ajou_terrain'),
    path('modifier-terrain/<int:terrain_id>/', views.modifier_terrain, name='modifier_terrain'),
    path('terrain/<int:terrain_id>/', views.terrain_details, name='terrain_details'),
    path('supprimer-terrain/<int:terrain_id>/', views.supprimer_terrain, name='supprimer_terrain'),
    path('modifier_utilisateur/', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('reserve/', views.reserver, name='reserve_terrain'),
    path('modifier_utilisateur_normal/', views.modifier_utilisateur_normal, name='modifier_utilisateur_normal'),
    path('envoyer_reservation/', views.envoyer_reservation, name='envoyer_reservation'),
    path('facture/<int:facture_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('fact/<int:reservation_id>/', views.fact, name='fact'),
    path('blog/', views.blog, name='blog'),
    path('annuler_reservation/<int:reservation_id>/', views.annuler_reservation, name='annuler_reservation'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
