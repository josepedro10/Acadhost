from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Usuario 
from .forms import UsuarioForm, UsuarioEditForm, UserProfileEditForm #

# USUARIO CRUD

@login_required
@permission_required('usuarios.delete_usuario', raise_exception=True) 
def index(request):
    usuarios = Usuario.objects.all().order_by('nome') 
    return render(request, 'usuarios/index.html', {'usuarios': usuarios})

def add(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            return redirect('usuarios_index')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/add.html', {'form': form})

@login_required
@permission_required('usuarios.delete_usuario', raise_exception=True) 
def detail(request, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)
    return render(request, 'usuarios/detail.html', {'usuario': usuario})

@login_required
@permission_required('usuarios.change_usuario', raise_exception=True)
def update(request, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuarios_index')
    else:
        form = UsuarioEditForm(instance=usuario)
    return render(request, 'usuarios/update.html', {'form': form})

@login_required
@permission_required('usuarios.delete_usuario', raise_exception=True)
def delete(request, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)
    usuario.delete()
    return redirect('usuarios_index')

@login_required
def edit_profile(request):
    usuario = request.user # Pega o usuário logado
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('user_profile_detail', id_usuario=usuario.id) # Redireciona para os detalhes do próprio usuário
    else:
        form = UserProfileEditForm(instance=usuario)
    return render(request, 'usuarios/profile_edit.html', {'form': form, 'usuario': usuario}) # Passa 'usuario' para o template

@login_required
@permission_required('usuarios.view_usuario', raise_exception=True) 
def detail_profile(request, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)
    return render(request, 'usuarios/profile_detail.html', {'usuario': usuario})