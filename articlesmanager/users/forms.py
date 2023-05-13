from django import forms
from .models import CustomUser, Position


class CreateUsersForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'middle_name', 'position', 'email', 'password', ]

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class': 'form-control'})

        self.fields['password'].label = 'Пароль'



class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'middle_name', 'position', 'email', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class': 'form-control'})


class ResetPasswordForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['password', ]

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].label = 'Новый пароль'
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
