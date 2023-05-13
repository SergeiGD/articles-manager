from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].label = 'Пароль'

        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].label = 'Логин'
