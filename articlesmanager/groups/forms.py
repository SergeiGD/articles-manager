from django import forms
from .models import UserGroup


class GroupsForm(forms.ModelForm):
    class Meta:
        model = UserGroup
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
