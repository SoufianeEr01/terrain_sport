from django import forms
from django.contrib.auth.models import User

class UserUpdateForm_n(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Ancien mot de passe" )
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Nouveau mot de passe", required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmer le nouveau mot de passe", required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password1 != new_password2:
            self.add_error('new_password2', "Les nouveaux mots de passe ne correspondent pas.")