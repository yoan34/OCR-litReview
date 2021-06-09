from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

    class Meta:
        labels = {
            'username': 'pseudo',
            'password': 'mot de passe',
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Répété le mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': "nom d'utilisateur",
            'email': 'adresse mail',
        }
        help_texts = {
            'username': None,
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
