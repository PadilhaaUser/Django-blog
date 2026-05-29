from django import template

register = template.Library()

MONTHS = {
    'Jan': 'jan.',
    'Feb': 'fev.',
    'Mar': 'mar.',
    'Apr': 'abr.',
    'May': 'mai.',
    'Jun': 'jun.',
    'Jul': 'jul.',
    'Aug': 'ago.',
    'Sep': 'set.',
    'Oct': 'out.',
    'Nov': 'nov.',
    'Dec': 'dez.',
}

@register.filter
def format_pt_short_date(value):
    if not value:
        return ''

    month = value.strftime('%b')
    month = MONTHS.get(month, month)
    return f"{value.day} {month} {value.year}"
