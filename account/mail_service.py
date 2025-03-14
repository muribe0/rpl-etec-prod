from django.core.mail import send_mail
from django.conf import settings


def send_confirmation_email(user):
    email = user.email
    user_pk = user.pk
    token = int(hash(user.username))
    token = token if token > 0 else -token
    subject = 'Confirmación de registro'
    message = f'Por favor, confirma tu registro en el siguiente enlace: ' \
              f'https://{settings.DOMAIN}/account/register/confirm/{user_pk}/{token}/'

    return send_mail(subject, message, None, ['rpl.etec@gmail.com'], fail_silently=False)


