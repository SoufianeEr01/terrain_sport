from django import forms
from .models import Terrain

class TerrainForm(forms.ModelForm):
    class Meta:
        model = Terrain
        fields = ['nom', 'adresse', 'tarif_horaire', 'disponibilite', 'capacite_joueur', 'map', 'image']
