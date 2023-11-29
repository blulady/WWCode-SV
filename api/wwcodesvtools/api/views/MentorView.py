from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from api.permissions import CanAccessMentor
from api.models import Mentor
from api.serializers.HostSerializer import MentorSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import logging
from rest_framework.response import Response
from rest_framework import status
from django.db.models.functions import Collate
from django.http import Http404

logger = logging.getLogger('django')


class MentorView(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsAuthenticated & CanAccessMentor]
    filter_class = [OrderingFilter, SearchFilter]
    ordering_fields = ['last_name']
    ordering = ['last_name']
    search_fields = ['^']