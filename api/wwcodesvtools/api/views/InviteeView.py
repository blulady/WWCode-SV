from api.models import Invitee
from api.serializers.InviteeSerializer import InviteeSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.permissions import CanAccessInvitee
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from uuid import uuid4
from api.helper_functions import send_email_helper
from datetime import datetime
import logging
from django.utils.http import urlencode
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.models import User

logger = logging.getLogger('django')


class InviteeViewSet(viewsets.ModelViewSet):
    # Exclude the invitees that has been accepted
    queryset = Invitee.objects.exclude(accepted=True)
    permission_classes = [IsAuthenticated & CanAccessInvitee]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'resend':
            return None
        return InviteeSerializer

    ERROR_CREATING_INVITEE = 'Error creating invitee'
    ERROR_SENDING_EMAIL_NOTIFICATION = 'Error sending email notification to the invitee'
    ERROR_RESENDING_REGISTRATION_INVITATION = 'Something went wrong during resend to invitee'
    INVITEE_CREATED_SUCCESSFULLY = 'Invitee Created Succesfully'
    INVITEE_DELETED_SUCCESSFULLY = 'Invitee Deleted Succesfully'
    INVITEE_NOT_FOUND = 'Invitee not found in database'
    INVITEE_RESEND_SUCCESSFUL = 'Resend registration invitation successful'
    INVITEE_NOT_FOUND = 'Requested id not found in Invitee database'

    post_response_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Invitee created and email sent successfully",
            examples={
                "application/json": {
                    'result': INVITEE_CREATED_SUCCESSFULLY,
                    'token': "0148f55a1f404363bf27dd8ebc9443c920210210220436"
                }
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    'error': {
                        "email": ["Enter a valid email address."],
                        "role": ["Invalid pk \"n\" - object does not exist."]
                    }
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Internal Server Error",
            examples={
                "application/json": {
                     'error': ERROR_CREATING_INVITEE
                }
            }
        ),
        status.HTTP_502_BAD_GATEWAY: openapi.Response(
            description="Bad Gateway",
            examples={
                "application/json": {
                    'error': ERROR_SENDING_EMAIL_NOTIFICATION
                }
            }
        ),
    }

    @swagger_auto_schema(request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                'email': openapi.Parameter('email', openapi.IN_BODY, description="Email", type=openapi.TYPE_STRING),
                                'role': openapi.Parameter('role', openapi.IN_BODY, description="Role", type=openapi.TYPE_INTEGER),
                                'message': openapi.Parameter('message', openapi.IN_BODY, description="Message", type=openapi.TYPE_STRING)
                             },
                         ),
                         operation_description="POST /invitee/",
                         responses=post_response_schema)
    @transaction.atomic
    def create(self, request):
        res_status = None
        error = None
        req = request.data
        logger.debug(f'InviteeViewSet Create : query params: {req}')
        email = req.get('email')
        role = req.get('role')
        message = req.get('message')

        try:
            timenow = datetime.now().strftime('%Y%m%d%H%M%S')
            # generate random token as a 32-character hexadecimal string and timestamp
            registration_token = str(uuid4().hex) + timenow
            created_by = request.user.id
            logger.debug(f'InviteeViewSet Create: token ={registration_token} : created_by ={created_by}')

            invitee_data = {
                "email": email,
                "message": message,
                "role": role,
                "status": 'INVITED',
                "registration_token": registration_token,
                "resent_counter": 0,
                "accepted": False,
                'created_at': timenow,
                'updated_at': timenow,
                'created_by': created_by
            }

            # create invitee in the invitee table
            serializer_invitee = InviteeSerializer(data=invitee_data)
            if serializer_invitee.is_valid():
                # creating txn savepoint
                sid = transaction.savepoint()
                serializer_invitee.save()
                logger.info('InviteeViewSet Create: Invitee data valid')
                # If invitee created successfully, then send email notification to the new invitee
                message_sent = self.send_email_notification(email, registration_token, message)
                if message_sent:
                    # all well, commit data to the db
                    transaction.savepoint_commit(sid)
                    res_status = status.HTTP_200_OK
                    logger.info('InviteeViewSet Create : Invitee created and email sent successfully')
                else:
                    # something went wrong sending the email, don't commit data to db, rollback txn
                    transaction.savepoint_rollback(sid)
                    res_status = status.HTTP_502_BAD_GATEWAY
                    error = self.ERROR_SENDING_EMAIL_NOTIFICATION
                    logger.info('InviteeViewSet Create : email NOT sent, invitee rolled back')
            else:
                # invalid data
                error = serializer_invitee.errors
                res_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            error = self.ERROR_CREATING_INVITEE
            logger.error(f'InviteeViewSet Create: {error}: {e}')
            res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if (error is None and res_status == status.HTTP_200_OK):
            return Response({'result': self.INVITEE_CREATED_SUCCESSFULLY, 'token': registration_token}, status=res_status)
        return Response({'error': error}, status=res_status)

    def send_email_notification(self, email, token, message):
        registration_link = f'{settings.FRONTEND_APP_URL}/register?{urlencode({"email": email, "token": token})}'
        logger.debug(f'InviteeViewSet Create: registrationt link {registration_link}')
        context_data = {"user": email,
                        "registration_link": registration_link,
                        "optional_message": message
                        }
        return send_email_helper(
            email, 'Invitation to Join Chapter Portal, Action Required', 'new_member_email.html', context_data)

    post_resend_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Registration Invitation resent successfully",
            examples={
                "application/json": {
                    'result': INVITEE_RESEND_SUCCESSFUL,
                    'token': "0148f55a1f404363bf27dd8ebc9443c920210210220436"
                }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Id not found in Invitee database",
            examples={
                "application/json": {
                    'result': INVITEE_NOT_FOUND,
                    'token': "0148f55a1f404363bf27dd8ebc9443c920210210220436"
                }
            }
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Error resending registration invitation",
            examples={
                "application/json": {
                    'result': INVITEE_NOT_FOUND,
                    'token': "0148f55a1f404363bf27dd8ebc9443c920210210220436"
                }
            }
        ),
    }

    @swagger_auto_schema(responses=post_resend_schema)
    @action(methods=['patch'], detail=True)
    def resend(self, request, *args, **kwargs):
        error = None
        invitee_id = kwargs.get('pk')
        target_invitee = get_object_or_404(Invitee, pk=invitee_id)
        logger.debug("invitee exists or 404", target_invitee)
        requestor = User.objects.get(email=request.user.email)

        try:
            message = "Resending registration invitation"
            timenow = datetime.now().strftime('%Y%m%d%H%M%S')
            target_invitee.created_by = requestor
            target_invitee.resent_counter += 1
            target_invitee.registration_token = str(uuid4().hex) + timenow
            message_sent = self.send_email_notification(target_invitee.email, target_invitee.registration_token, message)
            if message_sent:
                target_invitee.save()
                logger.info('InviteeViewSet Resend: Invitee registration invitation resent successfully')
                res_status = status.HTTP_200_OK
            else:
                res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
                error = self.ERROR_RESENDING_REGISTRATION_INVITATION
        except Exception as e:
            error = e
            logger.error(f'InviteeViewSet Resend: error: {e}')
            res_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        if error is None and res_status == status.HTTP_200_OK:
            return Response({'result': self.INVITEE_RESEND_SUCCESSFUL}, status=res_status)
        return Response({'Error': str(error)}, status=res_status)

    post_delete_schema = {
        status.HTTP_200_OK: openapi.Response(
            description="Invitee deleted successfully",
            examples={
                "application/json": {
                    'result': INVITEE_DELETED_SUCCESSFULLY,
                    'token': "0148f55a1f404363bf27dd8ebc9443c920210210220436"
                }
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Invitee not found in database",
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            description="Internal Server Error",
            examples={
                "application/json": {
                    'result': 'Internal server error.',
                    'token': "0148f55a1f404363bf27dd8ebc9443c920210210220436"
                }
            }
        ),
    }

    @swagger_auto_schema(responses=post_delete_schema)
    def destroy(self, request, *args, **kwargs):
        error = None
        try:
            invitee_obj = self.get_object()
            invitee_obj.delete()
            res_status = status.HTTP_200_OK
        except Exception as e:
            error = "Delete invitee failed. Invitee not found in database."
            logger.error(f'InviteeViewSet Destroy: {error}: {e}')
            res_status = status.HTTP_404_NOT_FOUND

        if (error is None):
            return Response({'Result': 'Invitee deleted successfully'}, status=res_status)
        else:
            return Response({'Result': str(error)}, status=res_status)
