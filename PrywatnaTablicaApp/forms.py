from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import MemoriesModel


class MemoryForm(ModelForm):
    class Meta:
        model = MemoriesModel
        exclude = ('title', 'date', 'archived')

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Override/modify fields
        instance.title = instance.get_title

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username.label = 'Nazwa użytkownika'
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password.label = 'Hasło użytkownika'


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Podaj adres email'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Wybierz nazwę użytkownika'
        })
        self.fields['username'].label = 'Nazwa użytkownika'

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Wpisz hasło'
        })
        self.fields['password1'].label = 'Hasło'

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Potwierdź hasło'
        })
        self.fields['password2'].label = 'Potwierdzenie hasła:'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Podany email już istnieje.")
        return email
