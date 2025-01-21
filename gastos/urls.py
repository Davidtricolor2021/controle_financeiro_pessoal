from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_despesas, name='listar_despesas'), # Página inicial
    path('adicionar/', views.adicionar_despesa, name='adicionar_despesa'), # Adicionar despesa
]
