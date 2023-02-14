from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from apps.core.lib.serializers import make_serializer_class


class Pagination(LimitOffsetPagination):
    pass


class BaseModelViewSet(ModelViewSet):
    pagination_class = Pagination

    def paginate_queryset(self, queryset):
        if "nopagination" in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)


def make_model_viewset(model):
    class ViewSet(BaseModelViewSet):
        queryset = model.objects.all()
        serializer_class = make_serializer_class(model)

    ViewSet.__name__ = f"{model.__name__}ViewSet"
    return ViewSet
