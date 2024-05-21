from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserUpdateForm_n(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Ancien mot de passe")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Nouveau mot de passe", required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirmer le nouveau mot de passe", required=False)

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
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if old_password:
            if not self.instance.check_password(old_password):
                self.add_error('old_password', "L'ancien mot de passe est incorrect.")

        if new_password1 and new_password1 != new_password2:
            self.add_error('new_password2', "Les nouveaux mots de passe ne correspondent pas.")
