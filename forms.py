from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from .models import UserProfile

class CustomErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="alert alert-danger">%s</div>' % ''.join(['<div>%s</div>' % e for e in self])

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    region = forms.ChoiceField(
        choices=UserProfile.REGION_CHOICES,
        required=True,
        help_text="Select your region to see trending movies in your area"
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "region")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Update or create user profile with selected region
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.region = self.cleaned_data['region']
            profile.save()
        return user

class UpdateRegionForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['region']
        widgets = {
            'region': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'region': 'Select Your Region'
        }
        help_texts = {
            'region': 'Choose the region where you live to see trending movies in your area'
        }
