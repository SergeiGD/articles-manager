from django import forms
from .models import Article
from states.models import State


class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'file', 'unique', 'bibliography', 'quoting', ]

    current_state = forms.ChoiceField()
    file = forms.FileField(widget=forms.FileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        STATUS_CHOICES = [(status.id, status.name) for status in State.objects.filter(date_deleted=None)]
        self.fields['current_state'].choices = STATUS_CHOICES

        if self.instance is not None and self.instance.id is not None:
            self.initial['current_state'] = self.instance.get_current_state().id

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({
            'class': 'form-control',
            'is_initial': False,
            'accept': 'application/pdf, .doc, .docx'
        })
        self.fields['file'].label = 'Файл'
        self.fields['unique'].widget.attrs.update({'class': 'metrics form-control'})
        self.fields['quoting'].widget.attrs.update({'class': 'metrics form-control'})
        self.fields['bibliography'].widget.attrs.update({'class': 'form-control other'})
        self.fields['current_state'].widget.attrs.update({'class': 'form-select'})
        self.fields['current_state'].label = 'Статус'
