from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.listar_despesas, name='listar_despesas'), # Página inicial
    path('adicionar/', views.adicionar_despesa, name='adicionar_despesa'), # Adicionar despesa
]
