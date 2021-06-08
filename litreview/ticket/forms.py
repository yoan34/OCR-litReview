from django import forms
from django.forms import widgets
from ticket.models import Review, Ticket

class UserFollowsForm(forms.Form):
    username = forms.CharField()

    class Meta:
        labels = {
            'username': "nom d'utilisateur",
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        CHOICES = [
            ('0', '0'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ]
        model = Review
        fields = ('rating', 'headline', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'style': 'resize:none;'}),
            'rating': forms.RadioSelect(choices=CHOICES)
        }
        labels = {
            'rating': 'Note',
            'headline': 'Titre',
            'body': 'description',
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        labels = {
            'title': 'Titre',
        }