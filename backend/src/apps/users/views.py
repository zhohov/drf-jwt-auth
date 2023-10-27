from dataclasses import dataclass, field
from typing import Type

from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


@dataclass
class UserDataClass:
    model: Type[models.Model] = User
    serializer_class: Type[serializers.ModelSerializer] = UserSerializer
    permission_classes: list = field(default_factory=lambda: [AllowAny, ])


class UsersList(UserDataClass, views.APIView):
    """
    List all users, or create a new user.
    """
    @extend_schema(tags=['UsersList'])
    def get(self, request) -> Response:
        queryset = self.model.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(tags=['UsersList'])
    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetail(UserDataClass, views.APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk: int) -> User:
        try:
            return self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    @extend_schema(tags=['UserDetail'])
    def get(self, request, pk: int) -> Response:
        queryset = self.get_object(pk=pk)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)

    @extend_schema(tags=['UserDetail'])
    def put(self, pk: int = None) -> None:
        ...

    @extend_schema(tags=['UserDetail'])
    def delete(self, pk: int = None) -> None:
        ...

