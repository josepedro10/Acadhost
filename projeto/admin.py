from django.contrib import admin
from .models import Projeto, Tag, ProjetoTag

admin.site.register(Projeto)
admin.site.register(Tag)
admin.site.register(ProjetoTag)
