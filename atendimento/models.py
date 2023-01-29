from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Atendente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cabine = models.CharField(max_length=100)

class TipoAtendimento(models.Model):
    prefixo = models.CharField(max_length=3)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
    

class Atendimento(models.Model):
    nome_cliente = models.CharField(max_length=255, verbose_name='Digite seu nome')
    data_atendimento = models.DateField(auto_now_add=True)    
    status_atendimento = models.CharField(max_length=255, default='fila')
    numero_senha = models.IntegerField()
    atendente = models.ForeignKey(Atendente, on_delete=models.PROTECT, null=True,blank= True)
    tipo_atendimento = models.ForeignKey(TipoAtendimento, on_delete=models.CASCADE)

    def gerar_senha(self):
        tipo_atendimento = self.tipo_atendimento
        ultima_senha = Atendimento.objects.filter(tipo_atendimento=tipo_atendimento).order_by('-numero_senha').first()
        if ultima_senha:
            self.numero_senha = ultima_senha.numero_senha + 1
            if self.numero_senha > 999:
                self.numero_senha = 1
        else:
            self.numero_senha = 1
        return f'{self.tipo_atendimento.prefixo}{str(self.numero_senha).zfill(3)}'
    
    def emAtendimento(self):
        self.status_atendimento = 'em atendimento'
        self.save()
    
    def finalizar(self):
        self.status_atendimento = 'finalizado'
        self.save()
