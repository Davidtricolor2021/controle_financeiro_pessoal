from django.shortcuts import render, redirect
from .models import Despesa, Categoria
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import calendar

@login_required
def listar_despesas(request):
    despesas = Despesa.objects.filter(usuario=request.user)
    return render(request, 'gastos/listar_despesas.html', {'despesas': despesas})

@login_required
def adicionar_despesa(request):
    if request.method == 'POST':
        data_pgto = request.POST['data_pgto']
        data_compra = request.POST['data_compra']
        descricao = request.POST['descricao']
        valor = float(request.POST.get('valor'))
        categoria_id = request.POST['categoria']
        parcelas = int(request.POST.get('parcelas', 1))  # Se não informado, assume 1 parcela

        # Obtem a categoria correspondente
        categoria = Categoria.objects.get(id=categoria_id)

        # Converte as datas para objetos datetime
        data_pgto_obj = datetime.strptime(data_pgto, '%Y-%m-%d')
        data_compra_obj = datetime.strptime(data_compra, '%Y-%m-%d')

        # Divide o valor total pelo número de parcelas
        valor_parcela = valor / parcelas

        # Cria as despesas para cada parcela
        for i in range(parcelas):
            # Ajusta a data de pagamento para os meses seguintes
            nova_data_pgto = data_pgto_obj + timedelta(days=i * calendar.monthrange(data_pgto_obj.year, data_pgto_obj.month)[1])

        # Cria a despesa
            Despesa.objects.create(
                data_pgto=nova_data_pgto,
                data_compra=data_compra_obj,
                descricao=f"{descricao} (Parcela {i + 1}/{parcelas})",
                valor=round(valor_parcela, 2),
                categoria=categoria,
                usuario=request.user
            )

        return redirect('listar_despesas')
    
    categorias = Categoria.objects.all()
    return render(request, 'gastos/adicionar_despesa.html', {'categorias': categorias})
