from django.urls import path
from . import views

urlpatterns = [
    path('gerar-senha/', views.gerar_senha, name='gerar_senha'),
    path('atendente/', views.ocioso, name='atendente'),
    path('chamar-proxima-senha/', views.chamar_proxima_senha, name='chamar_proxima_senha'),
    path('em-atendimento/', views.proximo, name='proximo'),
    path('em-atendimento/<id>', views.emAtendimento, name='em-atendimento'),
    path('finalizar-atendimento/', views.finalizarSemAtendimento, name='finalizar-sem-atendimento'),
    path('finalizar-atendimento/<id>', views.finalizarAtendimento, name='finalizar-atendimento'),
    path('', views.senhas_chamadas, name='senhas_chamadas'),
    path('tabela-dados/', views.tabela_dados, name='tabela_dados'),
    path('tabela-dados-fila/', views.tabela_dados_fila, name='tabela_dados_fila'),
]
