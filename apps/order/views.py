import json

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.lib import views
from apps.core.lib import serializers

from apps.order import models


class LineSerializer(serializers.ModelSerializer):
    sub_total = serializers.ReadOnlyField()

    class Meta:
        model = models.Line
        fields = "__all__"


class LineViewSet(views.ModelViewSet):
    queryset = models.Line.objects.all()
    serializer_class = LineSerializer


class OrderSerializer(serializers.ModelSerializer):
    price = serializers.ReadOnlyField()
    lines = LineSerializer(many=True, source="line_set", read_only=True)

    class Meta:
        model = models.Order
        fields = "__all__"


class OrderViewSet(views.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = [
        "reference",
        "type",
    ]

    @action(detail=False, url_path="with-lines", methods=["POST"])
    def with_lines(self, request, *args, **kwargs):
        data = request.data.copy()
        lines_str = data.pop("lines", [])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        result = serializer.data
        lines = [eval(line) for line in lines_str]
        for line in lines:
            line["order"] = f"/api/orders/{result['id']}"
        line_serializer = LineSerializer(data=lines, many=True)
        line_serializer.is_valid(raise_exception=True)
        line_serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
