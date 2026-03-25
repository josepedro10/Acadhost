from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from usuarios.models import Usuario 
from .models import Projeto, Tag, ProjetoTag, Equipe # Import Equipe model
from .forms import ProjetoForm, TagForm, ProjetoTagForm

# PROJETO

@login_required
@permission_required('projeto.view_projeto', raise_exception=True) 
def index(request):
    if request.user.is_superuser: 
        projetos = Projeto.objects.all() 
    else: 
        # Filtra projetos onde o usuário é autor OU é membro da equipe
        projetos = Projeto.objects.filter(autor=request.user) | Projeto.objects.filter(membros=request.user)
        projetos = projetos.distinct() # Remove duplicatas se um usuário for autor e membro
    
    tags = Tag.objects.all().order_by('nome')
    return render(request, 'projeto/index.html', {'projetos': projetos, 'tags': tags})

@login_required
@permission_required('projeto.view_projeto', raise_exception=True) 
def detail(request, id_projeto):
    projeto = get_object_or_404(Projeto, id=id_projeto)
    # NOVO: Permite acesso se for superusuário, autor ou um membro do projeto
    if not request.user.is_superuser and projeto.autor != request.user and not projeto.membros.filter(pk=request.user.pk).exists():
        return redirect('projeto_index') # Redireciona se não tiver permissão
    
    return render(request, 'projeto/detail.html', {'projeto': projeto})

@login_required
@permission_required('projeto.add_projeto', raise_exception=True)
def add(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.autor = request.user 
            projeto.save()
            form.save_m2m() # Salva o campo 'tags'

            # NOVO: Manual handling para 'membros_selecionados' e 'orientador_selecionado'
            orientador_selecionado = form.cleaned_data.get('orientador_selecionado') # Use .get para campos opcionais
            membros_selecionados = form.cleaned_data['membros_selecionados']

            if orientador_selecionado:
                Equipe.objects.create(projeto=projeto, membro=orientador_selecionado, funcao='orientador')

            for membro_aluno in membros_selecionados:
                Equipe.objects.create(projeto=projeto, membro=membro_aluno, funcao='colaborador') # Alunos como colaboradores

            return HttpResponseRedirect('/projeto/')
    else:
        form = ProjetoForm()
    return render(request, 'projeto/add.html', {'form': form})

@login_required
@permission_required('projeto.change_projeto', raise_exception=True)
def update(request, id_projeto):
    projeto = get_object_or_404(Projeto, id=id_projeto)
    # Permite acesso se for superusuário, autor ou um membro do projeto
    if not request.user.is_superuser and projeto.autor != request.user and not projeto.membros.filter(pk=request.user.pk).exists():
        return redirect('projeto_index')
    
    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            form.save() # Salva campos principais e 'tags'
            
            # NOVO: Manual handling para 'membros_selecionados' e 'orientador_selecionado' na atualização
            # Primeiro, remove todas as relações Equipe para este projeto (exceto o autor, se o autor estiver na Equipe)
            # Assumimos que o autor NÃO é gerenciado por estes campos, ele é fixo.
            Equipe.objects.filter(projeto=projeto).delete() # Remove TUDO e recria para garantir consistência

            orientador_selecionado = form.cleaned_data.get('orientador_selecionado')
            membros_selecionados = form.cleaned_data['membros_selecionados']

            if orientador_selecionado:
                Equipe.objects.create(projeto=projeto, membro=orientador_selecionado, funcao='orientador')

            for membro_aluno in membros_selecionados:
                Equipe.objects.create(projeto=projeto, membro=membro_aluno, funcao='colaborador')

            return HttpResponseRedirect('/projeto/')
    else:
        form = ProjetoForm(instance=projeto)
    return render(request, 'projeto/update.html', {'form': form})

@login_required
@permission_required('projeto.delete_projeto', raise_exception=True)
def delete(request, id_projeto):
    projeto = get_object_or_404(Projeto, id=id_projeto)
    # Permite acesso se for superusuário, autor ou um membro do projeto
    if not request.user.is_superuser and projeto.autor != request.user and not projeto.membros.filter(pk=request.user.pk).exists():
        return redirect('projeto_index')
        
    Projeto.objects.filter(id=id_projeto).delete()
    return HttpResponseRedirect('/projeto/')

# TAG (Views para Tags não precisam de filtro por autor)

@login_required
@permission_required('projeto.view_tag', raise_exception=True) 
def tag_index(request):
    tags = Tag.objects.all().order_by('nome') 
    return render(request, 'projeto/tag_index.html', {'tags': tags})

@login_required
@permission_required('projeto.add_tag', raise_exception=True)
def tag_add(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projeto_index') 
    else:
        form = TagForm()
    return render(request, 'projeto/tag_add.html', {'form': form})

@login_required
@permission_required('projeto.view_tag', raise_exception=True) 
def tag_detail(request, id_tag):
    tag = get_object_or_404(Tag, id=id_tag)
    return render(request, 'projeto/tag_detail.html', {'tag': tag})

@login_required
@permission_required('projeto.change_tag', raise_exception=True) 
def tag_update(request, id_tag):
    tag = get_object_or_404(Tag, id=id_tag)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('projeto_index') 
    else:
        form = TagForm(instance=tag)
    return render(request, 'projeto/tag_update.html', {'form': form})

@login_required
@permission_required('projeto.delete_tag', raise_exception=True) 
def tag_delete(request, id_tag):
    Tag.objects.filter(id=id_tag).delete() 
    return redirect('projeto_index')

# PROJETO-TAG (Views de ProjetoTag não precisam de filtro por autor)

@login_required
def projeto_tag_index(request):
    relacoes = ProjetoTag.objects.all()
    return render(request, 'projeto/projetotag_index.html', {'relacoes': relacoes})

@login_required
@permission_required('projeto.add_projetotag', raise_exception=True)
def projeto_tag_add(request):
    if request.method == 'POST':
        form = ProjetoTagForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/projeto/projetotags/')
    else:
        form = ProjetoTagForm()
    return render(request, 'projeto/projetotag_add.html', {'form': form})