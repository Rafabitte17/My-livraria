from rest_framework.viewsets import ModelViewSet

from core.models import Compra
from core.serializers import CompraCreateUpdateSerializer, CompraSerializer


class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return CompraCreateUpdateSerializer
        return CompraSerializer
