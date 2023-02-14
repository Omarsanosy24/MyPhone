from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class BaseModelSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    str = serializers.ReadOnlyField(source="__str__")


def make_serializer_class(model_, *fields_):
    if not fields_:
        fields_ = "__all__"
    else:
        fields_ = ["id", "url", *fields_]

    class _Serializer(BaseModelSerializer):
        class Meta:
            model = model_
            fields = fields_

    _Serializer.__name__ = f"{model_.__name__}Serializer"
    return _Serializer


def make_info_serializer(model_, source, *fields_):
    class _Serializer(ModelSerializer):
        class Meta:
            model = model_
            fields = ["id", *fields_]

    _Serializer.__name__ = f"{model_.__name__}InfoSerializer"
    return _Serializer(read_only=True, source=source)
