from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from api.serializers.CompleteUserProfileSerializer import CompleteUserProfileSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
import logging
from rest_framework import status

logger = logging.getLogger('django')


class UserProfileView(RetrieveUpdateAPIView):
    """
    Get current logged in user's id. If valid, display profile information for that user. Return an error
    message if there is no id match in the DB.
    ------------------------------------------------
    photo can be null, blank or "/media/images/filename.extention".
    ---------------------------------------------------------------
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CompleteUserProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = None
    http_method_names = ['get', 'put']

    def get_serializer_class(self):
        try:
            return CompleteUserProfileSerializer
        except Exception:
            current_user = self.request.user
            return ("Exception: ", current_user, "not found.")

    get_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Complete user profile information of the logged in user",
            examples={
                "application/json": {
                    'result': {
                                "id": 7,
                                "first_name": "Alexander",
                                "last_name": "Brown",
                                "email": "alexanderbrown@example.com",
                                "status": "ACTIVE",
                                "highest_role": "LEADER",
                                "date_joined": "2021-05-25T00:00:52.353000Z",
                                "role_teams": [
                                    {
                                        "role_name": "LEADER"
                                    }
                                ],
                                "city": "San Francisco",
                                "state": "CA",
                                "country": "United States",
                                "timezone": "PST",
                                "bio": "",
                                "photo": "",
                                "slack_handle": "",
                                "linkedin": "https://www.linkedin.com/in/alexanderbrown/",
                                "instagram": "https://instagram.com/alexanderbrown?igshid=MzRlODBiNWFlZA==",
                                "facebook": "https://www.facebook.com/alexanderbrown",
                                "twitter": "https://mstdn.social/@alexanderbrown",
                                "medium": ""
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
    }

    @swagger_auto_schema(
        operation_summary="Logged in user's profile",
        responses=get_response_schema)
    def get(self, request):
        current_user = self.request.user
        curr_id = current_user.id
        user = User.objects.get(pk=curr_id)
        user_serializer = self.get_serializer(user)
        return Response(user_serializer.data)

    put_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="User Profile updated successfully.",
            examples={
                "application/json": {
                    'result': 'User Profile has been updated.',
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="The information given has an error",
            examples={
                "application/json": {
                    'error': {
                        "first_name": ["This field may not be blank.", "This field may not be null."],
                        "last_name": ["This field may not be blank.", "This field may not be null."],
                        "photo": ["The submitted data was not a file. Check the encoding type on the form."]
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
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Something went wrong",
            examples={
                "application/json": {
                    'error': ['Email sending failed.']
                }
            }
        ),
    }

    @swagger_auto_schema(operation_description="""
                           This function is able to update first name and last name as well as the fields on the User Profile table of the logged in user.
                           ------------------------------------------------
                           photo is not required and can be null or blank
                           ------------------------------------------------
                            email and date_joined are read only, they will not be updated.
                           ------------------------------------------------
                        """,
                         operation_summary="Updates the logged in user's User Profile.",
                         responses=put_response_schema)
    def put(self, request, *args, **kwargs):
        res_status = None
        error = None
        user = request.user
        serializer = CompleteUserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                serializer.save()
                res_status = status.HTTP_200_OK
            except Exception as e:
                error = e
                res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            error = serializer.errors
            res_status = status.HTTP_400_BAD_REQUEST
        if (error is None and res_status == status.HTTP_200_OK):
            return Response({'result': 'User Profile has been updated.'}, status=res_status)
        return Response({'error': str(error)}, status=res_status)
