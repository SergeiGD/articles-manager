from django import forms
from .models import Author


class AuthorsForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'middle_name', 'email']
