from django.db import models
from enum import Enum

from django.contrib.auth.models import User

class Internaute(models.Model):
    nom = models.CharField(max_length=100)
    tel = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    mot_de_passe = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nom

class Proprietaire(Internaute):
    pass

class Administrateur(Internaute):
    pass

class disponibilite(Enum):
    DISPONIBLE = 'Disponible'
    NON_DISPONIBLE = 'Non_disponible'
    RESERVE = 'Reservé'
    MAINTENANCE = 'Maintenance'

class Terrain(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    tarif_horaire = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilite = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in disponibilite], default=disponibilite.DISPONIBLE.value)
    capacite_joueur = models.PositiveIntegerField()

    map = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(null=True,blank=True, upload_to='images/')
    administrateur = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.nom

class Equipe(models.Model):
    nom = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.nom


class EtatReservation(Enum):
    PASSEE = 'Passée'
    CONFIRMEE = 'Confirmée'
    ANNULEE = 'Annulée'

class MethodePaiement(Enum):
    CARTE_CREDIT = 'Carte de crédit'
    VIREMENT_BANCAIRE = 'Virement bancaire'

class Reservation(models.Model):

    montant_payer = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    etat = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in EtatReservation], default=EtatReservation.PASSEE.value )
    date_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    terrain_id = models.ForeignKey('Terrain', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Réservation {self.id} - {self.etat}"

class Facture(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    methode_paiement = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in MethodePaiement])
    reservations = models.OneToOneField('Reservation', on_delete=models.CASCADE, default=None, blank=True)

    def __str__(self):
        return f"Facture {self.id} - Montant: {self.montant}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.name} ({self.email}) - {self.created_at}"
