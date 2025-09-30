from django import forms
from .models import Petition

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['movie_title', 'description', 'reason']
        widgets = {
            'movie_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Provide a brief description of the movie (plot, genre, year, etc)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain why this movie should be added to our catalog'
            }),
        }
        labels = {
            'movie_title': 'Movie Title',
            'description': 'Movie Description',
            'reason': 'Why should we add this movie?',
        }