from django.core.mail import send_mail
from django.conf import settings


def send_confirmation_email(user):
    """
    Sends a confirmation email to the user with a link to confirm the registration.
    Generates a token based on the user's username hash.
    The token is sent as a parameter in the confirmation link.
    The idea is for the token to be sent to the user's inbox and is a way to verify that the user has access to the email.
    :param user: The user to send the email to
    """
    user_pk = user.pk
    token = int(hash(user.username))
    token = token if token > 0 else -token
    subject = 'Confirmación de registro'
    message = f'Por favor, confirma tu registro copiando esto en el enlace de la pagina: \n\n' \
              f'https://{settings.NAME_DOMAIN}/account/register/confirm/{user_pk}/{token}/ \n\n' \
              f'Si no te registraste, ignora este mensaje.'

    return send_mail(subject, message, None, [user.email], fail_silently=False)
