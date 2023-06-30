from rest_framework.response import Response
from rest_framework.viewsets import mixins, GenericViewSet


class ListModelMixin(mixins.ListModelMixin, GenericViewSet):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveModelMixin(mixins.RetrieveModelMixin, GenericViewSet):
    def retrieve(self: GenericViewSet, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=200)


class CreateModelMixin(mixins.CreateModelMixin, GenericViewSet):
    def perform_create(self: GenericViewSet, serializer):
        serializer.save()


class UpdateModelMixin(mixins.UpdateModelMixin, GenericViewSet):
    def perform_update(self: GenericViewSet, serializer):
        serializer.save()


class DestroyModelMixin(mixins.DestroyModelMixin, GenericViewSet):
    def perform_delete(self: GenericViewSet, instance):
        instance.delete()
