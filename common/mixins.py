from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ListModelMixin(object):
    def list(self: GenericViewSet, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveModelMixin(object):
    def retrieve(self: GenericViewSet, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=200)


class CreateModelMixin(object):
    def perform_create(self: GenericViewSet, serializer):
        serializer.save()


class UpdateModelMixin(object):
    def perform_update(self: GenericViewSet, serializer):
        serializer.save()


class DestroyModelMixin(object):
    def perform_delete(self: GenericViewSet, instance):
        instance.delete()
