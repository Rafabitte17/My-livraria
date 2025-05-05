from attrs import field
from cffi import model
from rest_framework.serializers import ModelSerializer

from core.models import Livro


class LivroSerializer(ModelSerializer):
    class Meta:
        model = Livro
        field = '__all__'
        depth = 1


class LivroListRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Livro
        fields = "__all__"
        depth = 1