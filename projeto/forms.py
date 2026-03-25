# acadhost/projeto/forms.py (Atualizado)

from django import forms
from django.forms import ModelForm, TextInput, Textarea, ModelMultipleChoiceField, Select, SelectMultiple, CheckboxSelectMultiple
from .models import Projeto, Tag, ProjetoTag, Equipe 
from usuarios.models import Usuario 

class ProjetoForm(ModelForm):
    # Campo para Tags (mantido como botões)
    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('nome'), 
        widget=CheckboxSelectMultiple(), # Mantido CheckboxSelectMultiple
        required=False,
        label="Tags"
    )

    # Campo para Alunos Membros (DE VOLTA para CheckboxSelectMultiple, como Tags)
    membros_selecionados = ModelMultipleChoiceField(
        queryset=Usuario.objects.filter(tipo='aluno').order_by('nome'), # FILTRADO PARA ALUNOS
        widget=CheckboxSelectMultiple(), # DE VOLTA PARA CheckboxSelectMultiple
        required=False,
        label="Alunos Membros do Projeto"
    )

    # Campo para Orientador (Select2 pesquisável, sem checklist) - Mantido Select
    orientador_selecionado = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(tipo='orientador').order_by('nome'), # FILTRADO PARA ORIENTADORES
        widget=Select(attrs={'class': 'form-control select2-single', 'data-placeholder': "Selecione um orientador"}), 
        required=False,
        empty_label="Selecione um orientador", 
        label="Orientador do Projeto"
    )

    class Meta:
        model = Projeto
        fields = [
            'nome', 'introducao', 'resumo', 'referencial_teorico', 'desenvolvimento',
            'resultados', 'conclusao', 'referencias', 'tags', 
        ]
        widgets = {
            'nome': TextInput(attrs={'class': 'form-control'}),
            'introducao': Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'resumo': Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'referencial_teorico': Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'desenvolvimento': Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'resultados': Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'conclusao': Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'referencias': Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk: 
            self.fields['tags'].initial = [
                tag.pk for tag in self.instance.tags.all()
            ]
            # Pré-selecionar membros (alunos)
            self.fields['membros_selecionados'].initial = [
                equipe_member.membro.pk for equipe_member in self.instance.equipe_set.filter(funcao='colaborador')
            ]
            # Pré-selecionar orientador
            try:
                orientador_equipe = self.instance.equipe_set.get(funcao='orientador')
                self.fields['orientador_selecionado'].initial = orientador_equipe.membro.pk
            except Equipe.DoesNotExist:
                pass

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['nome']
        widgets = {
            'nome': TextInput(attrs={'maxlength': 30, 'class': 'form-control'}),
        }

class ProjetoTagForm(ModelForm):
    class Meta:
        model = ProjetoTag
        fields = ['projeto', 'tag']
        widgets = {
            'projeto': Select(attrs={'class': 'form-control'}),
            'tag': Select(attrs={'class': 'form-control'}),
        }

class EquipeForm(ModelForm):
    class Meta:
        model = Equipe
        fields = ['membro', 'projeto', 'funcao']
        widgets = {
            'membro': Select(attrs={'class': 'form-control'}),
            'projeto': Select(attrs={'class': 'form-control'}),
            'funcao': Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['membro'].queryset = Usuario.objects.filter(is_active=True).order_by('username')
        self.fields['projeto'].queryset = Projeto.objects.order_by('nome')
        self.fields['membro'].label = "Membro"
        self.fields['projeto'].label = "Projeto"
        self.fields['funcao'].label = "Função na equipe"