from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "usuarios_index"),
    path('add/', views.add, name = "usuarios_add"),
    path('delete/<int:id_usuario>/', views.delete, name = "usuarios_delete"),
    path('update/<int:id_usuario>/', views.update, name = "usuarios_update"),
    path('<int:id_usuario>/', views.detail, name = "usuarios_detail"),
    path('profile/edit/', views.edit_profile, name='user_profile_edit'),
    path('profile/<int:id_usuario>/', views.detail_profile, name='user_profile_detail'), 
]