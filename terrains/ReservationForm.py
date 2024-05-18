from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['montant_payer', 'etat', 'date_debut', 'date_fin', 'client_id', 'terrain_id']
