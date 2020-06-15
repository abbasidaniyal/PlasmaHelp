import threading

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives

from plasma_for_covid.settings import EMAIL_HOST_USER


class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(
            self.subject, self.body, self.from_email, self.recipient_list
        )
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)


def send_mail(
    subject, body, from_email, recipient_list, fail_silently=False, html=None,
):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


def send_mail_to_user(request, user):
    email_subject = "Activate Your Account"
    domain = request.get_host()

    message = render_to_string(
        "activate_account.html",
        {
            "user": user,
            "domain": domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": TokenGenerator().make_token(user),
        },
    )
    send_mail(email_subject, message, EMAIL_HOST_USER, [user.email])
