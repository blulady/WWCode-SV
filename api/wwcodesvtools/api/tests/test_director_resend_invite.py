from django.test import TransactionTestCase
from django.core import mail
from ..helper_functions import send_email_helper


class DirectorResendInviteViewTestCase(TransactionTestCase):
    def test_send_request_to_director(self):
        to_email = 'WWCodeSV@gmail.com'
        subject = 'Request Director Resend Invite'
        template_file = 'reinvite_request.html'
        portal_link = "f'{settings.FRONTEND_APP_URL}/login"
        msg_to_director = "Use the link below to navigate to the login page to resend the invite."
        context_data = {"creator": "Director",
                        "email": "volunteer_3@example.com",
                        "role": "Volunteer",
                        "portal_link": portal_link,
                        "optional_message": msg_to_director,
                        "salutation": 'Thank you',
                        }
        send_email_helper(to_email, subject, template_file, context_data)

        # Test that the message has been sent.
        self.assertEquals(len(mail.outbox), 1)
