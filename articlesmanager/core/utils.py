from enum import Enum
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime
from smtplib import SMTPException


def send_email(subject: str, content: str, send_to: str):
    """
    Отправка писем
    :param subject: тема письма
    :param content: контент письма
    :param send_to: получатель
    :return:
    """
    # если в настройках указано не отправлять письма, то только отправка производится не будет
    email = EmailMessage(
        subject=subject,
        body=content,
        to=[send_to, ],
    )
    email.send()
