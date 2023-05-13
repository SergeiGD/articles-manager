from django import forms
from .models import Voting
from django.utils import timezone


class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting
        fields = ['date_start', 'date_end', ]
        widgets = {
            'date_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        form_data = self.cleaned_data
        date_start = form_data.get('date_start')
        date_end = form_data.get('date_end')

        if date_start > date_end:
            raise forms.ValidationError({'date_start': 'Дата начала должна быть раньше даты конца'})

        return form_data

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is not None and self.instance.pk is not None:
            self.initial['date_start'] = timezone.make_naive(self.instance.date_start).isoformat()
            self.initial['date_end'] = timezone.make_naive(self.instance.date_end).isoformat()
