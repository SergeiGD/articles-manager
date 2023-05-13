from django import forms
from .models import Author


class AuthorsForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'middle_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class': 'form-control'})