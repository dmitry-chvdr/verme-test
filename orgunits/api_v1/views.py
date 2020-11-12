"""
Copyright 2020 ООО «Верме»
"""

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from orgunits.api_v1.serializers import OrganizationSerializer
from orgunits.models import Organization
from wfm.views import TokenAuthMixin


class OrganizationViewSet(TokenAuthMixin, ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

    @action(methods=["GET"], detail=True)
    def parents(self, request, pk=None):
        """
        Возвращает родителей запрашиваемой организации
        TODO: Написать два действия для ViewSet (parents и children), используя методы модели
        """
        try:
            organization = Organization.objects.get(pk=pk)
            parents = organization.parents()
            response = OrganizationSerializer(parents, many=True)
            return Response(response.data, status=status.HTTP_200_OK)
        except Organization.DoesNotExist:
            return Response("Organization does not exist", status=status.HTTP_404_NOT_FOUND)

    @action(methods=["GET"], detail=True)
    def children(self, request, pk=None):
        try:
            organization = Organization.objects.get(pk=pk)
            children = organization.children()
            response = OrganizationSerializer(children, many=True)
            return Response(response.data, status=status.HTTP_200_OK)
        except Organization.DoesNotExist:
            return Response("Organization does not exist", status=status.HTTP_404_NOT_FOUND)
