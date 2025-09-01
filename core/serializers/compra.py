from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,  # novo
    HiddenField,  # novo
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)
from core.models import Compra, ItensCompra


class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade')

    def validate_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValidationError('A quantidade deve ser maior do que zero.')
        return quantidade

    def validate(self, item):
        if item['quantidade'] > item['livro'].quantidade:
            raise ValidationError('Quantidade de itens maior do que a quantidade em estoque.')
        return item


class CompraCreateUpdateSerializer(ModelSerializer):
    class CompraCreateUpdateSerializer(ModelSerializer):
        usuario = HiddenField(default=CurrentUserDefault())

        class Meta:
            model = Compra
            fields = ('id', 'usuario', 'itens')

        def create(self, validated_data):
            itens_data = validated_data.pop('itens')
            compra = Compra.objects.create(**validated_data)
            for item_data in itens_data:
                ItensCompra.objects.create(compra=compra, **item_data)
            compra.save()
            return compra


class ItensCompraListSerializer(ModelSerializer):
    livro = CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = ItensCompra
        fields = ('quantidade', 'livro')
        depth = 1


class CompraListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItensCompraListSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')


class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.quantidade * instance.livro.preco

    class Meta:
        model = ItensCompra
        fields = ('id', 'quantidade', 'total', 'livro')
        depth = 2


class CompraSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'status', 'total', 'itens')
