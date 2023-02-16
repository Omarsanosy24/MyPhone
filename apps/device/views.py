from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from apps.core.lib import views
from apps.device import models
from apps.device import serializers
from apps.device import services


def retrieve_related(request, model, queryset):
    serializer = serializers.serializers.make_serializer_class(model)(
        instance=queryset,
        many=True,
        context={"request": request},
    )
    return Response(serializer.data)


class Company(views.ModelViewSet):
    serializer_class = serializers.Company
    queryset = models.Company.objects.all()
    search_fields = [
        "name",
    ]

    @action(detail=True)
    def products(self, request, *args, **kwargs):
        """Retrieve all products for the current company."""
        return retrieve_related(
            request, models.Product, self.get_object().product_set.all(),
        )


class Category(views.ModelViewSet):
    serializer_class = serializers.Category
    queryset = models.Category.objects.all()
    search_fields = [
        "name",
    ]

    @action(detail=True)
    def products(self, request, *args, **kwargs):
        """Retrieve all products for the current company."""
        return retrieve_related(
            request, models.Product, self.get_object().product_set.all(),
        )


class Product(views.ModelViewSet):
    serializer_class = serializers.Product
    queryset = models.Product.objects.all()
    search_fields = [
        "name",
        "company__name",
    ]

    @action(detail=True)
    def series(self, request, *args, **kwargs):
        """Retrieve all series for the current product."""
        return retrieve_related(
            request, models.Series, self.get_object().series_set.all(),
        )


class Series(views.ModelViewSet):
    serializer_class = serializers.Series
    queryset = models.Series.objects.all()
    search_fields = [
        "name",
        "product__name",
        "product__company__name",
    ]

    @action(detail=True)
    def models(self, request, *args, **kwargs):
        """Retrieve all models for the current series."""
        return retrieve_related(
            request, models.Model, self.get_object().model_set.all(),
        )


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
        OpenApiExample("sample", [
            {"Storage": "256G", "Color": "Red", "price": "100", "id": "1"}
        ]),
    ])
    @action(detail=True, url_path="available-variants")
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
    search_fields = ["name"]


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
