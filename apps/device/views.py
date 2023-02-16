from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiResponse
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.lib import views
from apps.device import models, services, serializers


class Company(views.ModelViewSet):
    serializer_class = serializers.Company
    queryset = models.Company.objects.all()
    search_fields = [
        "name",
    ]


class Category(views.ModelViewSet):
    serializer_class = serializers.Category
    queryset = models.Category.objects.all()
    search_fields = [
        "name",
    ]


class Product(views.ModelViewSet):
    serializer_class = serializers.Product
    queryset = models.Product.objects.all()
    search_fields = [
        "name",
        "company__name",
    ]


class Series(views.ModelViewSet):
    serializer_class = serializers.Series
    queryset = models.Series.objects.all()
    search_fields = [
        "name",
        "product__name",
        "product__company__name",
    ]


class Model(views.ModelViewSet):
    serializer_class = serializers.Model
    queryset = models.Model.objects.all()
    search_fields = [
        "name",
        "series__name",
        "series__product__name",
        "series__product__company__name",
    ]

    @extend_schema(examples=[
        OpenApiExample("", {"Storage": ["128G"], "Color": ["Red"]}),
    ])
    @action(detail=True)
    def variants(self, *args, **kwargs):
        """Retrieve the existing variants, even if not in stock."""
        model = self.get_object()
        data = services.get_variants(model)
        return Response(data)

    @extend_schema(examples=[
        OpenApiExample("", [{"Storage": "256G", "Color": "Red"}]),
    ])
    @action(detail=True)
    def available_variants(self, *args, **kwargs):
        """Retrieve the variants existing in stock for this model."""
        model = self.get_object()
        data = services.get_available_variants(model)
        return Response(data)


class VariantGroup(views.ModelViewSet):
    serializer_class = serializers.VariantGroup
    queryset = models.VariantGroup.objects.all()
    search_fields = ["name"]


class VariantValue(views.ModelViewSet):
    serializer_class = serializers.VariantValue
    queryset = models.VariantValue.objects.all()
    search_fields = ["value"]


class ModelVariant(views.ModelViewSet):
    serializer_class = serializers.ModelVariant
    queryset = models.ModelVariant.objects.all()
    filterset_fields = [
        "model__name",
        "model__id",
    ]
    search_fields = [
        "model__name",
        "model__series__name",
        "model__series__product__name",
        "model__series__product__company__name",
        "values__value",
    ]


class Device(views.ModelViewSet):
    serializer_class = serializers.Device
    queryset = models.Device.objects.all()
    search_fields = [
        "imei",
        "serial_number",
        "model_variant__model__name",
        "model_variant__model__series__name",
        "model_variant__model__series__product__name",
        "model_variant__model__series__product__company__name",
        "model_variant__values__value",
    ]
