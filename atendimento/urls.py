from django.urls import path
from . import views

urlpatterns = [
    path('gerar-senha/', views.gerar_senha, name='gerar_senha'),
    path('chamar-proxima-senha/', views.chamar_proxima_senha, name='chamar_proxima_senha'),
    path('finalizar-atendimento/', views.finalizarSemAtendimento, name='finalizar-sem-atendimento'),
    path('finalizar-atendimento/<id>', views.finalizarAtendimento, name='finalizar-atendimento'),
    path('', views.senhas_chamadas, name='senhas_chamadas'),
    path('tabela-dados/', views.tabela_dados, name='tabela_dados'),
]
