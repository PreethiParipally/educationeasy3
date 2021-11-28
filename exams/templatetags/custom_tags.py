from django import template

register = template.Library()

@register.filter(is_safe=True)
def sum_total_marks(value):
    sum = 0 
    print("helllo",value)
    for v in value:
        sum += v.marks
    return sum