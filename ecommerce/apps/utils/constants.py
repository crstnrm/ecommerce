from os import environ
from enum import Enum


SERVICE = environ.get('SERVICE', 'ses')
REGION = environ.get('SERVICE', 'us-east-1')
SENDER = environ.get('SERVICE', 'sender <sender@sender.com>')
CONFIGURATION = environ.get('SERVICE', 'ConfigSet')
CHARSET = environ.get('SERVICE', 'UTF-8')


class NotificationTemplate(Enum):
    DEFAULT = 'templates/notification.html'
