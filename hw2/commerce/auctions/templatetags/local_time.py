from django import template
from tzlocal import get_localzone # pip install tzlocal
from django.utils import timezone

register = template.Library()

@register.filter
def toLocalTime(value):
    local_tz = get_localzone()
    timezone.activate(local_tz)
    return timezone.localtime(value)