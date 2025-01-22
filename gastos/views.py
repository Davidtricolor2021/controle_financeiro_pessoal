from django.shortcuts import render, redirect
from .models import Despesa, Categoria
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
import calendar

def login_view(request):
    if request.user.is_authenticated:
        # Se já estiver logado, redireciona para a página principal
        return redirect('listar_despesas')  # ou qualquer outra página desejada
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Faz o login e redireciona para a página principal
            user = form.get_user()
            login(request, user)
            return redirect('listar_despesas')  # ou qualquer outra página desejada
    else:
        form = AuthenticationForm()

    return render(request, 'gastos/login.html', {'form': form})

@login_required
def listar_despesas(request):
    # Agrupar as despesas por mês/ano
    despesas_por_mes = defaultdict(list)
    despesas = Despesa.objects.filter(usuario=request.user).annotate(mes=TruncMonth('data_pgto'))

    # Organizar as despesas por mês
    for despesa in despesas:
        key = despesa.data_pgto.strftime('%Y-%m')  # Exemplo: "2025-01"
        despesas_por_mes[key].append(despesa)

    # Ordenar os meses de forma cronológica
    despesas_por_mes = dict(sorted(despesas_por_mes.items()))

    # Gerar os nomes dos meses (Exemplo: "Jan/2025")
    meses_formatados = {
        key: despesa[0].data_pgto.strftime('%b/%Y')  # Exemplo: "Jan/2025"
        for key, despesa in despesas_por_mes.items()
    }

    return render(request, 'gastos/listar_despesas.html', {
        'despesas_por_mes': despesas_por_mes,
        'meses_formatados': meses_formatados,
    })

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
            nova_data_pgto = data_pgto_obj + relativedelta(months=i)

        # Cria a despesa
            Despesa.objects.create(
                data_pgto=nova_data_pgto,
                data_compra=data_compra_obj,
                descricao=descricao,
                #descricao=f"{descricao} (Parcela {i + 1}/{parcelas})",
                valor=round(valor_parcela, 2),
                categoria=categoria,
                parcela_atual=f"{i + 1}",
                parcelas=parcelas,
                usuario=request.user
            )

        return redirect('listar_despesas')
    
    categorias = Categoria.objects.all()
    return render(request, 'gastos/adicionar_despesa.html', {'categorias': categorias})
