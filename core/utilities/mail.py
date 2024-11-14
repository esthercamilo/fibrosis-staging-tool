from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, message, recipient_list, from_email=None):
    """
    Envia um e-mail.

    :param subject: Assunto do e-mail.
    :param message: Corpo do e-mail.
    :param recipient_list: Lista de destinatários.
    :param from_email: E-mail do remetente (opcional).
    """
    if from_email is None:
        from_email = settings.EMAIL_HOST_USER

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
