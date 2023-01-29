from django.shortcuts import render, redirect
from .forms import GerarSenhaForm
from .models import Atendimento, TipoAtendimento, Atendente
from django.http import JsonResponse
# Create your views here.

def gerar_senha(request):
    form = GerarSenhaForm()
    print(request.method)
    if request.method == "POST":
        form = GerarSenhaForm(request.POST)
        if form.is_valid():
            atendimento = form.save(commit=False)
            atendimento.gerar_senha()
            atendimento.status_atendimento='fila'
            atendimento.save()
            form = GerarSenhaForm()
            context={'form': form, 'tipos_atendimento': TipoAtendimento.objects.all(), 'atendimento': atendimento}
            return render(request, 'gerar_senha.html', context)
        else:
            print('merda2')  
            print(form.errors)
    else:
        print('merda')        
    context={'form': form, 'tipos_atendimento': TipoAtendimento.objects.all()}
    return render(request, 'gerar_senha.html', context)

def chamar_proxima_senha(request):
    atendente = Atendente.objects.get(user=request.user)    
    if request.method == 'POST':        
        atendente.cabine = request.POST.get('cabine')
        atendente.save()
    try:
        senha_atual = Atendimento.objects.filter(status_atendimento='fila', tipo_atendimento__nome='Preferencial').order_by('data_atendimento').first()
        if not senha_atual:
            senha_atual = Atendimento.objects.filter(status_atendimento='fila').order_by('data_atendimento').first()
        else: print(senha_atual)
        senha_atual.status_atendimento = 'chamando'
        senha_atual.atendente = atendente    
        senha_atual.save()
    except:
        senha_atual=Atendimento.objects.filter(status_atendimento='chamando', atendente=atendente).order_by('data_atendimento').first()
    return render(request, 'proxima_senha.html', {'senha': senha_atual})

def senhas_chamadas(request):
    senhas = Atendimento.objects.filter(status_atendimento='chamando').order_by('-data_atendimento')[:10]
    context = {'senhas': senhas}
    return render(request, 'senhas_chamadas.html', context)


def tabela_dados(request):
    # atendimentos = Atendimento.objects.filter(status_atendimento='chamando').order_by('data_atendimento').first()
    atendimentos = Atendimento.objects.all()
    dados = [
        {
            'senha': f'{atendimento.tipo_atendimento.prefixo}'+str(atendimento.numero_senha).zfill(4),
            'cabine': atendimento.atendente.cabine,
            'cliente': atendimento.nome_cliente,
            'status': atendimento.status_atendimento
        }
        for atendimento in atendimentos if atendimento.status_atendimento == 'chamando'
    ]
    return JsonResponse(dados, safe=False)

def finalizarAtendimento(request, id):
    try:
        atendimento = Atendimento.objects.get(id=id)
        atendimento.finalizar()
    except:
        pass
    return redirect('chamar_proxima_senha')

def finalizarSemAtendimento(request):
    return redirect('chamar_proxima_senha')