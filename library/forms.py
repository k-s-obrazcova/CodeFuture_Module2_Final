from django import forms
import re

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from library.models import Publishing_house


class Publishing_houseForm(forms.ModelForm):
    class Meta:
        model = Publishing_house
        fields = (
            'title',
            'agent_name',
            'agent_last_name',
            'agent_surname',
            'telephone',
        )
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form_control'}
            ),
            'agent_name': forms.TextInput(
                attrs={'class': 'form_control'}
            ),
            'agent_last_name': forms.TextInput(
                attrs={'class': 'form_control'}
            ),
            'agent_surname': forms.TextInput(
                attrs={'class': 'form_control'}
            ),
            'telephone': forms.TextInput(
                attrs={'class': 'form_control'}
            ),
        }
    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        #+7(XXX)XXX-XX-XX
        if re.match(r'\+7\(\d{3}\)\d{3}-\d{2}-\d{2}', telephone):
            return telephone
        raise ValidationError('Телефон не соответствует шаблону +7(ХХХ)ХХХ-ХХ-ХХ')

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
        username = forms.CharField(
            label='Логин пользователя',
            widget=forms.TextInput(attrs={'class': 'form-control',}),
            min_length=2
        )
        email = forms.EmailField(
            label='Электронная почта',
            widget=forms.EmailInput(attrs={'class': 'form-control', })
        )
        password1 = forms.CharField(
            label='Введите пароль',
            widget=forms.PasswordInput(attrs={'class': 'form-control', })
        )
        password2 = forms.CharField(
            label='Повторите пароль',
            widget=forms.PasswordInput(attrs={'class': 'form-control', })
        )

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=2
    )
    password = forms.CharField(
        label='Пароль пользователя',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )