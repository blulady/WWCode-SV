from api.models import Invitee
from rest_framework.response import Response
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from api.helper_functions import send_email_helper
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

import logging

logger = logging.getLogger('django')


class DirectorResendInviteView(GenericAPIView):
    permission_classes = [AllowAny]

    USER_DOES_NOT_EXIST = "There is no user with this email address in the Invitee database."
    SEND_EMAIL_FAILED = "Server got an invalid response from the email server"
    RESEND_INVITE_SUCCESS = "Success. Resent invitation to requestor"
    INTERNAL_SERVER_ERROR = "Server encountered an unexpected condition that prevented it from fulfilling the request: {error}"

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Send reinvite successfully",
            examples={
                "application/json": {
                    'result': RESEND_INVITE_SUCCESS
                }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="User not found in Invitee database",
            examples={
                "application/json": {
                    'error': USER_DOES_NOT_EXIST
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Server encountered an unexpected condition that prevented it from fulfilling the request",
            examples={
                "application/json": {
                    'error': INTERNAL_SERVER_ERROR
                }
            }
        ),
        status.HTTP_502_BAD_GATEWAY: openapi.Response(
            description="Server got an invalid response from email server",
            examples={
                "application/json": {
                    'error': SEND_EMAIL_FAILED
                }
            }
        ),
    }
    email_param = openapi.Parameter('email', openapi.IN_QUERY, description="Email", type=openapi.TYPE_STRING)

    @swagger_auto_schema(responses=post_response_schema, manual_parameters=[email_param],
                         operation_summary="Send an email to the director to request a new registration link",
                         operation_description="Send an email to the director who created the invitee for the given email asking to resend a new registration link")
    def get(self, request):
        status_msg = None
        error = None
        try:
            request_email = self.request.query_params.get('email')
            # Check that requestor is in the Invitee table.
            check_invitee = Invitee.objects.filter(email=request_email).exists()
            if not check_invitee:
                res_msg = self.USER_DOES_NOT_EXIST
                status_msg = status.HTTP_404_NOT_FOUND
                return Response({'error': res_msg}, status=status_msg)
            else:
                invitee = Invitee.objects.get(email=request_email)
                to_email = invitee.created_by.email
                msg_to_director = 'Use the link below to navigate to the login page to resend the invite.'
                portal_link = f'{settings.FRONTEND_APP_URL}/login'
                context_data = {'creator': 'Director',
                                'email': request_email,
                                'role': invitee.role,
                                'portal_link': portal_link,
                                'optional_message': msg_to_director,
                                }
                result = send_email_helper(
                    to_email, 'Request to resend an invitation', 'reinvite_request.html', context_data
                )
                if result:
                    res_msg = self.RESEND_INVITE_SUCCESS
                    status_msg = status.HTTP_200_OK
                else:
                    error = self.SEND_EMAIL_FAILED
                    res_msg = error
                    status_msg = status.HTTP_502_BAD_GATEWAY

            if error is None:
                return Response({'result': res_msg}, status=status_msg)
            return Response({'error': res_msg}, status=status_msg)
        except Exception as e:
            logger.error(f'DirectorResendInviteView: error: {e}')
            res_msg = self.INTERNAL_SERVER_ERROR.format(error=str(e))
            status_msg = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response({'error': res_msg}, status=status_msg)
