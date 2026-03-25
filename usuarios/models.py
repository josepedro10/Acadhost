
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class Usuario(AbstractUser):

    TIPOS = (
        ('aluno', 'Aluno'),
        ('orientador', 'Orientador'),
        ('avaliador', 'Avaliador'),
    )

    nome = models.CharField(max_length=100)
    idade = models.PositiveIntegerField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    matricula = models.CharField(max_length=20, unique=True, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, blank=True, null=True)
    add_em = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.nome} - ({self.tipo})'

    def save(self, *args, **kwargs):
        # Passo 1: Armazene o tipo antigo antes de salvar a instância atualizada
        old_tipo = None
        if self.pk: # Se o objeto já existe (é uma atualização)
            try:
                old_instance = Usuario.objects.get(pk=self.pk)
                old_tipo = old_instance.tipo
            except Usuario.DoesNotExist:
                pass # Objeto novo, não há tipo antigo para se preocupar

        # Passo 2: Chame o método save() original para salvar a instância do Usuario
        super().save(*args, **kwargs)

        # Passo 3: Atribua o usuário ao grupo correto após o salvamento
        if self.tipo: # Se um tipo foi definido para o usuário
            # Encontra o nome de exibição do tipo (ex: 'Aluno' para a chave 'aluno')
            group_name = next((display for key, display in self.TIPOS if key == self.tipo), None)

            if group_name:
                # Se o tipo mudou, remove o usuário do grupo anterior (se houver)
                if old_tipo and old_tipo != self.tipo:
                    old_group_name = next((display for key, display in self.TIPOS if key == old_tipo), None)
                    if old_group_name:
                        try:
                            old_group = Group.objects.get(name=old_group_name)
                            self.groups.remove(old_group)
                        except Group.DoesNotExist:
                            pass # O grupo antigo não existe, não faz nada

                # Adiciona o usuário ao grupo correspondente ao seu tipo atual
                group, created = Group.objects.get_or_create(name=group_name)
                self.groups.add(group)

