from django.shortcuts import render, redirect
from .forms import GerarSenhaForm
from .models import Atendimento, TipoAtendimento, Atendente
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def gerar_senha(request):
    form = GerarSenhaForm()    
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
    context={'form': form, 'tipos_atendimento': TipoAtendimento.objects.all()}
    return render(request, 'gerar_senha.html', context)

@login_required
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
    return render(request, 'proxima_senha.html', {'senha': senha_atual, 'cabine': atendente.cabine})

login_required
def chamar_proxima_senha_especifica(request, prefixo):
    atendente = Atendente.objects.get(user=request.user)    
    if request.method == 'POST':        
        atendente.cabine = request.POST.get('cabine')
        atendente.save()
    try:
        senha_atual = Atendimento.objects.filter(status_atendimento='fila', tipo_atendimento__prefixo=prefixo).order_by('data_atendimento').first()
        # if not senha_atual:
        #     senha_atual = Atendimento.objects.filter(status_atendimento='fila').order_by('data_atendimento').first()
        # else: print(senha_atual)
        senha_atual.status_atendimento = 'chamando'
        senha_atual.atendente = atendente    
        senha_atual.save()
    except:
        senha_atual=Atendimento.objects.filter(status_atendimento='chamando', atendente=atendente).order_by('data_atendimento').first()
    return render(request, 'proxima_senha.html', {'senha': senha_atual, 'cabine': atendente.cabine, 'prefixo': prefixo})

@login_required
def ocioso(request):
    atendente = Atendente.objects.get(user=request.user)    
    if request.method == 'POST':        
        atendente.cabine = request.POST.get('cabine')
        atendente.save()
    senha_atual=None
    return render(request, 'proxima_senha.html', {'senha': senha_atual, 'cabine': atendente.cabine})

@login_required
def ocioso_especifico(request, prefixo):
    atendente = Atendente.objects.get(user=request.user)    
    if request.method == 'POST':        
        atendente.cabine = request.POST.get('cabine')
        atendente.save()
    senha_atual=None
    return render(request, 'proxima_senha.html', {'senha': senha_atual, 'cabine': atendente.cabine, 'prefixo': prefixo})


@login_required
def senhas_chamadas(request):
    senhas = Atendimento.objects.filter(status_atendimento='chamando').order_by('-data_atendimento')[:10]
    context = {'senhas': senhas}
    return render(request, 'senhas_chamadas.html', context)

@login_required
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

@login_required
def tabela_dados_fila(request):
    # atendimentos = Atendimento.objects.filter(status_atendimento='chamando').order_by('data_atendimento').first()
    atendimentos = Atendimento.objects.all()
    dados = [
        {
            'senha': f'{atendimento.tipo_atendimento.prefixo}'+str(atendimento.numero_senha).zfill(4),            
            'cliente': atendimento.nome_cliente,
            'status': atendimento.status_atendimento
        }
        for atendimento in atendimentos if atendimento.status_atendimento == 'fila'
    ]
    return JsonResponse(dados, safe=False)

@login_required
def tabela_dados_fila_especifica(request, prefixo):
    # atendimentos = Atendimento.objects.filter(status_atendimento='chamando').order_by('data_atendimento').first()
    atendimentos = Atendimento.objects.all()
    dados = [
        {
            'senha': f'{atendimento.tipo_atendimento.prefixo}'+str(atendimento.numero_senha).zfill(4),            
            'cliente': atendimento.nome_cliente,
            'status': atendimento.status_atendimento
        }
        for atendimento in atendimentos if atendimento.status_atendimento == 'fila' and atendimento.tipo_atendimento.prefixo == prefixo
    ]
    return JsonResponse(dados, safe=False)

@login_required
def emAtendimento(request, id):
    try:
        atendimento = Atendimento.objects.get(id=id)
        atendimento.emAtendimento()
        context={
        'senha': atendimento,
        }        
    except:
        context={
        'senha': '',
        }
    return render(request, 'em-atendimento.html', context)

@login_required
def emAtendimentoEspecifico(request, id, prefixo):
    try:
        atendimento = Atendimento.objects.get(id=id)
        atendimento.emAtendimento()
        context={
        'senha': atendimento,
        'prefixo': prefixo
        }        
    except:
        context={
        'senha': '',
        'prefixo': prefixo
        }
    return render(request, 'em-atendimento.html', context)

@login_required
def finalizarAtendimento(request, id):
    try:
        atendimento = Atendimento.objects.get(id=id)
        atendimento.finalizar()
    except:
        pass
    return redirect('atendente')

@login_required
def finalizarAtendimentoEspecifico(request, id, prefixo):
    try:
        atendimento = Atendimento.objects.get(id=id)
        atendimento.finalizar()
    except:
        pass
    return redirect('atendente_especifico', prefixo)

@login_required
def proximo(request):
    return redirect('chamar_proxima_senha')

@login_required
def finalizarSemAtendimento(request):
    return redirect('chamar_proxima_senha')