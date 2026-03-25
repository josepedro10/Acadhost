# acadhost/usuarios/forms.py

from django.forms import ModelForm, TextInput, NumberInput, Select, Textarea, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # Para UsuarioForm
from .models import Usuario
from projeto.models import Projeto, Equipe

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'nome', 'idade', 'telefone', 'cpf', 'tipo', 'matricula', 'username' # Corrigido para 'password' e 'password2'
        ]
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}), # Campo 'password' para AbstractUser
            'password2': PasswordInput(attrs={'class': 'form-control'}), # Campo de confirmação
            'nome': TextInput(attrs={'class': 'form-control'}),
            'idade': NumberInput(attrs={'class': 'form-control'}),
            'telefone': TextInput(attrs={'class': 'form-control'}),
            'cpf': TextInput(attrs={'class': 'form-control'}),
            'matricula': TextInput(attrs={'class': 'form-control'}),
            'tipo': Select(attrs={'class': 'form-control'}),

        }

class UsuarioEditForm(ModelForm):
    class Meta:
        model = Usuario

        fields = ['username', 'nome', 'idade', 'telefone', 'cpf', 'matricula', 'tipo', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'nome': TextInput(attrs={'class': 'form-control'}),
            'idade': NumberInput(attrs={'class': 'form-control'}),
            'telefone': TextInput(attrs={'class': 'form-control'}),
            'cpf': TextInput(attrs={'class': 'form-control'}),
            'matricula': TextInput(attrs={'class': 'form-control'}),
            'tipo': Select(attrs={'class': 'form-control'}),

        }

class UserProfileEditForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ('username', 'nome', 'idade', 'telefone', 'cpf', 'matricula')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'nome': TextInput(attrs={'class': 'form-control'}),
            'idade': NumberInput(attrs={'class': 'form-control'}),
            'telefone': TextInput(attrs={'class': 'form-control'}),
            'cpf': TextInput(attrs={'class': 'form-control'}),
            'matricula': TextInput(attrs={'class': 'form-control'}),
        }
