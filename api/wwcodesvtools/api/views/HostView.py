from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from api.permissions import CanAccessHost
from api.models import Host
from api.serializers.HostSerializer import HostSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import logging
from rest_framework.response import Response
from rest_framework import status
from django.db.models.functions import Collate

logger = logging.getLogger('django')


class HostView(viewsets.ModelViewSet):
    """
    Returns a list of all Host Companies.
    ------------------------------------------------
    Ordering by company_name
    You may also specify reverse ordering by prefixing the field name with '-', like so:
    http//example.com/api/hosts/?ordering=company
    http//example.com/api/hosts/?ordering=-company
    -------------------------------------------------------------
    Search by any number of characters in company_name, contact_name or contact_email like so:
    http//example.com/api/hosts/?search=contact_name
    http//example.com/api/hosts/?search=contact_email
    http//example.com/api/hosts/?search=company_name
    ---------------------------------------------------------------
    Contact information
    The contacts associated with each Host Company are displayed as a list.
    Each contact is represented by a dictionary with the following keys: 'name', 'email', and 'info'.
    If a Host Company does not have any contacts, the list of contacts will be empty.
    ---------------------------------------------------------------
    """

    queryset = Host.objects.all()
    serializer_class = HostSerializer
    permission_classes = [IsAuthenticated & CanAccessHost]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['company']
    ordering = ['company']
    search_fields = ['^company_search', '^contacts__name', '^contacts__email']
    http_method_names = ['get', 'post', 'put', 'delete']

    ERROR_HOST_NOT_FOUND = 'Host Company does not exist.'
    ERROR_CREATING_HOST = 'Error creating Host Company.'
    ERROR_UPDATING_HOST = 'Error updating Host Company.'
    ERROR_DELETING_HOST = 'Error deleting Host Company.'
    HOST_CREATED_SUCCESSFULLY = 'Host Company Created Successfully.'
    HOST_UPDATED_SUCCESSFULLY = 'Host Company Updated Successfully.'
    HOST_DELETED_SUCCESSFULLY = 'Host Company Deleted Successfully.'

    get_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="List of all Host Companies",
            examples={
                "application/json": {
                    'result': [
                             {"id": 1,
                              "company": "appen",
                              "city": "San Jose",
                              "contacts": [
                                {
                                    "name": "Iris Green",
                                    "email": "iris@appen.com",
                                    "info": ""
                                },
                                {
                                    "name": "Rosemary Wolfe",
                                    "email": "rosemary@appen.com",
                                    "info": "Will be able to arrange food"
                                    }
                                ],
                              "notes": ""},
                             {"id": 2,
                              "company": "Apple",
                              "city": "Santa Clara",
                              "contacts": [],
                              "notes": "It is a long"}
                        ]
                }
            }
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description="User is not authenticated",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided.",
                }
            }
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="User is not allowed",
            examples={
                "application/json": {
                    "detail": "You do not have permission to perform this action.",
                }
            }
        ),
    }

    @swagger_auto_schema(
        operation_summary="Lists all Host Companies sorted ascending",
        responses=get_response_schema)
    def list(self, request):
        queryset = self.get_queryset()
        # Create an deterministic field for search
        queryset = queryset.annotate(company_search=Collate("company", "und-x-icu"))
        # Eliminate duplicate rows
        queryset = queryset.distinct()
        filter_query_set = self.filter_queryset(queryset)
        serializer = self.get_serializer_class()(filter_query_set, many=True)
        return Response(serializer.data)

    get_id_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Details of the specific Host Company",
            examples={
                "application/json": {
                    'result':
                             {"id": 1,
                              "company": "appen",
                              "city": "San Jose",
                              "contacts": [
                                {
                                    "name": "Iris Green",
                                    "email": "iris@appen.com",
                                    "info": ""
                                },
                                {
                                    "name": "Rosemary Wolfe",
                                    "email": "rosemary@appen.com",
                                    "info": "Will be able to arrange food"
                                    }
                                ],
                              "notes": ""}
                }
            }
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description="User is not authenticated",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided.",
                }
            }
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="User is not allowed",
            examples={
                "application/json": {
                    "detail": "You do not have permission to perform this action.",
                }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="id not found in Host database",
            examples={
                "application/json": {
                        "detail": "Not found.",
                }
            }
        ),
    }

    @swagger_auto_schema(
        operation_summary="Shows a specific Host Company",
        operation_description="This function retrieves the details of a specific Host Company based on its ID.",
        responses=get_id_response_schema)
    def retrieve(self, request, pk):
        instace = self.get_object()
        serializer = self.get_serializer_class()(instace)
        return Response(serializer.data)

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Host Company Created",
            examples={
                "application/json": {
                    'result': 'Host Company Created Successfully',
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="The information given has an error",
            examples={
                "application/json": {
                    'error': {
                        "company": ["host with this company already exists.", "This field may not be blank."],
                        "contacts": [{"email": ["Enter a valid email address."]}],
                    },
                }
            }
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description="User is not authenticated",
            examples={
                "application/json": {
                        "detail": "Authentication credentials were not provided.",
                }
            }
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="User is not allowed",
            examples={
                "application/json": {
                        "detail": "You do not have permission to perform this action.",
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Something went wrong",
            examples={
                "application/json": {
                     'error': 'Error creating Host Company'
                }
            }
        ),
    }

    @swagger_auto_schema(request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                'company': openapi.Parameter('company', openapi.IN_BODY, description="Company name", type=openapi.TYPE_STRING),
                                'city': openapi.Parameter('city', openapi.IN_BODY, description="City", type=openapi.TYPE_STRING),
                                'contacts': openapi.Parameter('contacts', openapi.IN_BODY, description="Company name", type=openapi.TYPE_ARRAY,
                                                              items=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                                                   properties={
                                                                                               'name': openapi.Parameter('name', openapi.IN_BODY, description="Contact name", type=openapi.TYPE_STRING),
                                                                                               'email': openapi.Parameter('email', openapi.IN_BODY, description="Contact email", type=openapi.TYPE_STRING),
                                                                                               'info': openapi.Parameter('info', openapi.IN_BODY, description="Info", type=openapi.TYPE_STRING),
                                                                                              })),
                                'notes': openapi.Parameter('notes', openapi.IN_BODY, description="Notes", type=openapi.TYPE_STRING)
                             },
                         ),
                         operation_summary="Creates a new Host Company",
                         operation_description="This function creates a new Host Company using the provided information.",
                         responses=post_response_schema)
    def create(self, request):
        res_status = None
        error = None
        data = request.data
        user = request.user
        company = data.get('company')
        try:
            host_data = {
                "company": company,
                "city": data.get('city'),
                "contacts": data.get('contacts'),
                "notes": data.get('notes'),
                "created_by": user.id,
                "updated_by": user.id,
            }
            serializer_host = HostSerializer(data=host_data)
            if serializer_host.is_valid():
                try:
                    serializer_host.save()
                    res_status = status.HTTP_200_OK
                except Exception as e:
                    error = e
                    res_status = status.HTTP_400_BAD_REQUEST
            else:
                # invalid data
                error = serializer_host.errors
                res_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            error = self.ERROR_CREATING_HOST
            logger.error(f'HostViewSet Create: {error}: {e}')
            res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if (error is None and res_status == status.HTTP_200_OK):
            return Response({'result': self.HOST_CREATED_SUCCESSFULLY}, status=res_status)
        return Response({'error': str(error)}, status=res_status)

    update_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Host Company Updated Successfully",
            examples={
                "application/json": {
                    'result': 'Host Company Updated Successfully.',
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="The information given has an error",
            examples={
                "application/json": {
                    'error': {
                        "company": ["host with this company already exists.", "This field may not be blank."],
                        "contacts": [{"email": ["Enter a valid email address."]}],
                    }
                }
            }
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description="User is not authenticated",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided.",
                }
            }
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="User is not allowed",
            examples={
                "application/json": {
                    "detail": "You do not have permission to perform this action.",
                }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="id not found in Host database",
            examples={
                "application/json": {
                    "detail": "Not found.",
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Something went wrong",
            examples={
                "application/json": {
                    'error': 'Error updating Host Company.'
                }
            }
        ),
    }

    @swagger_auto_schema(request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                'company': openapi.Parameter('company', openapi.IN_BODY, description="Company name", type=openapi.TYPE_STRING),
                                'city': openapi.Parameter('city', openapi.IN_BODY, description="City", type=openapi.TYPE_STRING),
                                'contacts': openapi.Parameter('contacts', openapi.IN_BODY, description="Company name", type=openapi.TYPE_ARRAY,
                                                              items=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                                                   properties={
                                                                                               'name': openapi.Parameter('name', openapi.IN_BODY, description="Contact name", type=openapi.TYPE_STRING),
                                                                                               'email': openapi.Parameter('email', openapi.IN_BODY, description="Contact email", type=openapi.TYPE_STRING),
                                                                                               'info': openapi.Parameter('info', openapi.IN_BODY, description="Info", type=openapi.TYPE_STRING),
                                                                                              })),
                                'notes': openapi.Parameter('notes', openapi.IN_BODY, description="Notes", type=openapi.TYPE_STRING)
                             },
                         ),
                         operation_summary="Updates a given Host Company",
                         operation_description="This function updates the information of a specific Host Company based on its ID.",
                         responses=update_response_schema)
    def update(self, request, *args, **kwargs):
        error = None
        res_status = None
        data = request.data
        user = request.user
        host_target = self.get_object()
        if host_target:
            try:
                host_data = {
                    "company": data.get('company'),
                    "city": data.get('city'),
                    "contacts": data.get('contacts'),
                    "notes": data.get('notes'),
                    "created_by": host_target.created_by.id,
                    "updated_by": user.id,
                }
                serializer_host = HostSerializer(host_target, data=host_data)
                if serializer_host.is_valid():
                    try:
                        serializer_host.save()
                        res_status = status.HTTP_200_OK
                    except Exception as e:
                        error = e
                        res_status = status.HTTP_400_BAD_REQUEST
                else:
                    # invalid data
                    error = serializer_host.errors
                    res_status = status.HTTP_400_BAD_REQUEST
            except Exception as e:
                error = self.ERROR_UPDATING_HOST
                logger.error(f'HostViewSet Update: {error}: {e}')
                res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            error = self.ERROR_HOST_NOT_FOUND
            res_status = status.HTTP_404_NOT_FOUND
        if (error is None and res_status == status.HTTP_200_OK):
            return Response({'result': self.HOST_UPDATED_SUCCESSFULLY}, status=res_status)
        return Response({'error': str(error)}, status=res_status)

    delete_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Deleted Successfully",
            examples={
                "application/json": {
                    'result': 'Host deleted successfully',
                }
            }
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description="Authentication Required",
            examples={
                "application/json": {
                        "detail": "Authentication credentials were not provided.",
                }
            }
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="No Permission",
            examples={
                "application/json": {
                        "detail": "You do not have permission to perform this action.",
                }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Host Not Found",
            examples={
                "application/json": {
                        "detail": "Host company not found in database.",
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Internal Server Error",
            examples={
                "application/json": {
                    'result': 'Internal server error.'
                }
            }
        ),
    }

    @swagger_auto_schema(
        operation_summary="Deletes a specified host company",
        operation_description="This function deletes an existing Host Company.",
        responses=delete_response_schema
    )
    def destroy(self, request, *args, **kwargs):
        try:
            host = self.get_object()
            host.delete()
            return Response({'result': self.HOST_DELETED_SUCCESSFULLY}, status=status.HTTP_200_OK)
        except Exception as e:
            error = "Host not found in database."
            logger.error(f'HostViewSet Destroy: {error}: {e}')
            return Response({'error': self.ERROR_HOST_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
