from django.contrib import admin
from .models import Cliente, Vinho, Pedido_Vinho, Pedido

admin.site.register(Cliente)
admin.site.register(Vinho)
admin.site.register(Pedido_Vinho)
admin.site.register(Pedido)