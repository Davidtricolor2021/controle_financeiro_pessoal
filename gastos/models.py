from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Despesa(models.Model):
    data_pgto = models.DateField()
    data_compra = models.DateField()
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    parcelas = models.PositiveIntegerField(default=1)  # Número total de parcelas
    parcela_atual = models.PositiveIntegerField(default=1)  # Número da parcela atual
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"
