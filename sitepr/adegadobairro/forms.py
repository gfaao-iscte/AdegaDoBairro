# forms.py
from django import forms
from .models import *


class VinhoForm(forms.ModelForm):
    class Meta:
        model = Vinho
        fields = ['nome', 'vinho_imagem', 'preco','tipo','regiao','colheita','produtor','precopromocao','descricao']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['morada', 'cidade', 'nif']