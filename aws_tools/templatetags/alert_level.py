from django import template
from django.contrib.messages import constants as message_constants


register = template.Library()


@register.simple_tag
def alert_level(message):
    if message.level == message_constants.ERROR:
        return 'danger'
    if message.level == message_constants.WARNING:
        return 'warning'
    if message.level == message_constants.SUCCESS:
        return 'success'
    if message.level == message_constants.INFO:
        return 'info'
    if message.level == message_constants.DEBUG:
        return 'secondary'
    return 'primary'
