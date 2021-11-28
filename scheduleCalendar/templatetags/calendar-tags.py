from django import template
from schedular.models import Schedule
 
register = template.Library()
 
@register.simple_tag
def total_events():
    return Schedule.objects.count()
