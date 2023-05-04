from django import forms
from .models import State


class StatesForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class': 'form-control'})
