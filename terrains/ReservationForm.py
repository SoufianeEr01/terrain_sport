from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['montant_payer', 'reservation_datetime', 'terrain_id', 'tarif_horaire']
        labels = {
            'reservation_datetime': 'Date et heure de réservation',
        }
        widgets = {
            'user': forms.HiddenInput(),
        }

    reservation_datetime = forms.DateTimeField(widget=forms.TextInput(attrs={
        'class': 'form-control datetimepicker',
        'style': 'color: white; background-color: grey;',
        'placeholder': 'AAAA-MM-JJ HH:mm'
    }))

    def clean_reservation_datetime(self):
        data = self.cleaned_data['reservation_datetime']
        minutes = data.minute
        if minutes % 15 != 0:
            raise ValidationError(
                "L'heure doit être arrondie à l'un des intervalles suivants : XX:00, XX:15, XX:30, XX:45.")
        return data