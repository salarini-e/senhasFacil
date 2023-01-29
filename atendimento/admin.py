from django.contrib import admin
from .models import Atendente, Atendimento, TipoAtendimento

# Register your models here.
admin.site.register(Atendente)
admin.site.register(TipoAtendimento)
admin.site.register(Atendimento)