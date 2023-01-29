from django import forms
from .models import Atendimento, TipoAtendimento

class GerarSenhaForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ['nome_cliente','tipo_atendimento']
        widgets = {
            'tipo_atendimento': forms.RadioSelect()
        }
    # nome_cliente = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nome do cliente'}))    
    # tipo_atendimento = forms.ModelChoiceField(queryset=TipoAtendimento.objects.all())
