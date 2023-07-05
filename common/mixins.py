import json
import logging
from collections import OrderedDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


logger = logging.getLogger("django.server")


class LoggerMixin:
    def request_logger(self: GenericViewSet, payload: OrderedDict = None):
        formatted_string = f"Request({self.action} - {self.request._request.path}) : {str(self.__class__)} / {payload}"
        logger.info(formatted_string)

    def response_logger(self: GenericViewSet, payload: ReturnDict = None):
        if self.action == "list":
            # If too much data logged, customize this function.
            payload = json.loads(json.dumps(payload))
        elif not payload:
            pass
        else:
            payload = dict(payload)
        formatted_string = f"Response({self.action} - {self.request._request.path}) : {str(self.__class__)} / {payload}"
        logger.info(formatted_string)
        

class ListModelMixin(mixins.ListModelMixin, LoggerMixin, GenericViewSet):
    def list(self, request, *args, **kwargs):
        self.request_logger(payload=request.data)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.response_logger(payload=serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.response_logger(payload=serializer.data)
        return Response(serializer.data)


class RetrieveModelMixin(mixins.RetrieveModelMixin, LoggerMixin, GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        self.request_logger()
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.response_logger(payload=serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateModelMixin(mixins.CreateModelMixin, LoggerMixin, GenericViewSet):
    def perform_create(self, serializer):
        self.request_logger(payload=self.request.data)
        serializer.save()
        self.response_logger()


class UpdateModelMixin(mixins.UpdateModelMixin, LoggerMixin, GenericViewSet):
    def perform_update(self, serializer):
        self.request_logger(payload=self.request.data)
        serializer.save()
        self.response_logger(payload=serializer.data)


class DestroyModelMixin(mixins.DestroyModelMixin, LoggerMixin, GenericViewSet):
    def perform_destroy(self, instance):
        self.request_logger(payload=instance)
        instance.delete()
        self.response_logger()


class MappingViewSetMixin(GenericViewSet):
    serializer_action_map = {}

    def get_serializer_class(self):
        if self.serializer_action_map.get(self.action, None):
            return self.serializer_action_map[self.action]
        return self.serializer_class
