from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer


def with_history(history_serializer_class: type[ModelSerializer] = None):
    def inner(model_viewset_class):
        add_history_action(
            model_viewset_class,
            get_history_serializer_class(
                history_serializer_class,
                model_viewset_class,
            ),
        )
        return model_viewset_class

    return inner


def add_history_action(model_viewset_class, history_serializer_class):
    def history(self, *args, **kwargs):
        obj = self.get_object()
        serializer = history_serializer_class(
            instance=obj.history.all(),
            many=True,
        )
        return Response(data=serializer.data)

    model_viewset_class.history = action(detail=True)(history)


def get_history_serializer_class(history_serializer_class, model_viewset_class):
    if history_serializer_class:
        return history_serializer_class

    class HistorySerializer(ModelSerializer):
        class Meta:
            model = model_viewset_class.queryset.model.history.model
            fields = "__all__"

    return HistorySerializer
