from rest_framework.viewsets import ModelViewSet

from core.models import Compra
from core.serializers import CompraCreateUpdateSerializer, CompraListSerializer, CompraSerializer


class CompraViewSet(ModelViewSet):
    # queryset = Compra.objects.order_by('-id')
    # serializer_class = CompraSerializer
    compra = Compra.objects.first()
    print(compra.tipo_pagamento)  # mostra o valor interno (ex: 1)
    print(compra.get_tipo_pagamento_display())  # mostra o valor legível (ex: 'Cartão de Crédito')

    def get_serializer_class(self):
        if self.action == 'list':
            return CompraListSerializer
        if self.action in {'create', 'update', 'partial_update'}:
            return CompraCreateUpdateSerializer
        return CompraSerializer

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser:
            return Compra.objects.order_by('-id')
        if usuario.groups.filter(name='administradores'):
            return Compra.objects.order_by('-id')
        return Compra.objects.filter(usuario=usuario).order_by('-id')
