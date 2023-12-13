# filters.py
from django import template
from datetime import datetime

register = template.Library()

@register.filter
def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
