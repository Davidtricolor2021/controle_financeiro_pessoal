from django import forms
from .models import Despesa

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['data_pgto', 'data_compra', 'categoria', 'descricao', 'valor', 'parcelas']
