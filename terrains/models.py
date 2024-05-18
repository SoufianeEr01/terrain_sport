from django.db import models
from enum import Enum
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
    disponibilite = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in disponibilite])
    capacite_joueur = models.PositiveIntegerField()
    superficie = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True,blank=True, upload_to='images/')
    latitude = models.FloatField()
    longitude = models.FloatField()
    administrateur = models.ForeignKey('Administrateur', on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

class Equipe(models.Model):
    nom = models.CharField(max_length=100)
    clients = models.ManyToManyField('Client', related_name='equipes')

    def __str__(self):
        return self.nom

class Client(Internaute):
    terrains = models.ManyToManyField('Terrain', through='Reservation', related_name='clients')

class EtatReservation(Enum):
    PASSEE = 'Passée'
    CONFIRMEE = 'Confirmée'
    ANNULEE = 'Annulée'

class MethodePaiement(Enum):
    CARTE_CREDIT = 'Carte de crédit'
    VIREMENT_BANCAIRE = 'Virement bancaire'

class Reservation(models.Model):
    montant_payer = models.DecimalField(max_digits=10, decimal_places=2)
    etat = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in EtatReservation], default=EtatReservation.PASSEE.value )
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    client_id = models.ForeignKey('Client', on_delete=models.CASCADE, default=None)
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
