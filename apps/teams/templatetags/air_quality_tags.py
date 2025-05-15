from django import template

register = template.Library()

@register.filter
def get_pm_card_color(pm_value, pm_type):
    try:
        pm = float(pm_value)
    except (ValueError, TypeError):
        return 'bg-secondary text-dark'

    if pm_type == "pm10":
        if pm <= 54:
            return "bg-success text-white"
        elif pm <= 154:
            return "bg-warning text-dark"
        elif pm <= 254:
            return "bg-orange text-dark"
        elif pm <= 354:
            return "bg-danger text-white"
        elif pm <= 424:
            return "bg-purple text-white"
        else:
            return "bg-maroon text-white"

    elif pm_type == "pm25":
        if pm <= 12:
            return "bg-success text-white"
        elif pm <= 35.4:
            return "bg-warning text-dark"
        elif pm <= 55.4:
            return "bg-orange text-dark"
        elif pm <= 150.4:
            return "bg-danger text-white"
        elif pm <= 250.4:
            return "bg-purple text-white"
        else:
            return "bg-maroon text-white"

    return "bg-secondary text-dark"
