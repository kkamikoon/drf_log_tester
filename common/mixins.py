import json
import logging
from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


logger = logging.getLogger("django.server")


class LoggerMixin:        
    def request_logger(self, class_name: str, function_name: str, payload: OrderedDict = None):
        formatted_string = f"Request({function_name}) : {class_name} / {payload}"
        logger.info(formatted_string)

    def response_logger(self, class_name:str, function_name: str, payload: ReturnDict):
        if function_name == "list":
            # If too much data logged, customize this function.
            payload = json.loads(json.dumps(payload))
        else:
            payload = dict(payload)
        formatted_string = f"Response({function_name}) : {class_name} / {payload}"
        logger.info(formatted_string)
        

class ListModelMixin(mixins.ListModelMixin, LoggerMixin, GenericViewSet):
    def list(self, request, *args, **kwargs):
        self.request_logger(class_name=self.__class__, function_name="list", payload=request.data)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.response_logger(class_name=self.__class__, function_name="list", payload=serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.response_logger(class_name=self.__class__, function_name="list", payload=serializer.data)
        return Response(serializer.data)


class RetrieveModelMixin(mixins.RetrieveModelMixin, GenericViewSet):
    def retrieve(self: GenericViewSet, request, *args, **kwargs):
        self.request_logger(class_name=self.__class__, function_name="retrieve")
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.response_logger(class_name=self.__class__, function_name="retrieve", payload=serializer.data)
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


class MappingViewSetMixin(object):
    serializer_action_map = {}

    def get_serializer_class(self):
        if self.serializer_action_map.get(self.action, None):
            return self.serializer_action_map[self.action]
        return self.serializer_class