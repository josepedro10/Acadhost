# acadhost/projeto/models.py (Atualizado)

from django.db import models

class Projeto(models.Model):
    autor = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='projetos_autoria')
    nome = models.CharField(max_length=200)
    introducao = models.TextField()
    resumo = models.TextField()
    referencial_teorico = models.TextField()
    desenvolvimento = models.TextField()
    resultados = models.TextField()
    conclusao = models.TextField()
    referencias = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        'Tag',
        through='ProjetoTag',
        related_name='projetos',
        blank=True
    )
    # NOVO CAMPO: Membros do projeto
    membros = models.ManyToManyField(
        'usuarios.Usuario',
        through='Equipe',
        related_name='projetos_participados', # Renomeado para clareza
        blank=True # Permite que o projeto não tenha membros inicialmente
    )

    def __str__(self):
        return self.nome

class Tag(models.Model):
    nome = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.nome

class ProjetoTag(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('projeto', 'tag')
        verbose_name = 'Projeto Tag'
        verbose_name_plural = 'Projetos Tags'
    def __str__(self):
        return f'{self.projeto.nome} → {self.tag.nome}'

class Equipe(models.Model):
    FUNCOES = (
        ('autor', 'Autor'),
        ('orientador', 'Orientador'),
        ('colaborador', 'Colaborador'),
    )
    membro = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    projeto = models.ForeignKey('projeto.Projeto', on_delete=models.CASCADE)
    funcao = models.CharField(max_length=20, choices=FUNCOES)
    data_entrada = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('membro', 'projeto')
        verbose_name = 'Membro da Equipe'
        verbose_name_plural = 'Membros da Equipe'

    def __str__(self):
        return f'{self.membro.username} - {self.projeto.nome} ({self.funcao})' # Usando username para consistência