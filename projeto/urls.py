from django.urls import path
from . import views

urlpatterns = [
    # Projeto
    path('', views.index, name='projeto_index'),
    path('<int:id_projeto>/', views.detail, name='projeto_detail'),
    path('add/', views.add, name='projeto_add'),
    path('update/<int:id_projeto>/', views.update, name='projeto_update'),
    path('delete/<int:id_projeto>/', views.delete, name='projeto_delete'),

    # Tag
    path('tag/', views.tag_index, name='tag_index'),
    path('tag/add/', views.tag_add, name='tag_add'),
    path('tag/update/<int:id_tag>/', views.tag_update, name='tag_update'),
    path('tag/delete/<int:id_tag>/', views.tag_delete, name='tag_delete'),

]
