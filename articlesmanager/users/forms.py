from django import forms
from .models import CustomUser


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

    # def save(self, commit=True):
    #     instance = CustomUser.objects.create_user(
    #         email = self.cleaned_data['email']
    #     )
    #     instance.flag1 = 'flag1' in self.cleaned_data['multi_choice']  # etc
    #     if commit:
    #         instance.save()
    #     return instance
