from rest_framework.exceptions import ValidationError

from apps.core.lib import serializers
from apps.device import models

Company = serializers.make_serializer_class(models.Company)
Category = serializers.make_serializer_class(models.Category)


class Product(serializers.ModelSerializer):
    companyInfo = serializers.make_info_serializer(models.Company, "company", "name")
    categoryInfo = serializers.make_info_serializer(models.Category, "category", "name")

    class Meta:
        model = models.Product
        fields = "__all__"


class CompanyProducts(serializers.ModelSerializer):
    products = serializers.make_serializer_class(Product)(many=True)


class Series(serializers.ModelSerializer):
    productInfo = serializers.make_info_serializer(models.Product, "product", "name")

    class Meta:
        model = models.Series
        fields = "__all__"


class Model(serializers.ModelSerializer):
    seriesInfo = serializers.make_info_serializer(models.Series, "series", "name")

    class Meta:
        model = models.Model
        fields = "__all__"


class ModelVariant(serializers.ModelSerializer):
    modelInfo = serializers.make_info_serializer(models.Model, "model", "name")

    class Meta:
        model = models.ModelVariant
        fields = "__all__"

    def validate_variant(self, value):
        if not models.ModelVariant.valid_variants(value):
            raise ValidationError("Only one value by variant group allowed")
        return value


VariantGroup = serializers.make_serializer_class(models.VariantGroup)
VariantValue = serializers.make_serializer_class(models.VariantValue)

Device = serializers.make_serializer_class(models.Device)
