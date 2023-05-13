from django import forms
from .models import Review


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'approved', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['comment'].widget.attrs.update({'class': 'form-control'})
        self.fields['approved'].widget.attrs.update({'class': 'form-check-input'})

