from django import template
from datetime import date

register = template.Library()

@register.filter
def detailed_age(past_date):
    if not past_date:
        return None

    today = date.today()

    years = today.year - past_date.year
    months = today.month - past_date.month
    days = today.day - past_date.day

    if days < 0:
        months -= 1
        days += (past_date.replace(month=today.month, day=1) - past_date.replace(day=1)).days

    if months < 0:
        years -= 1
        months += 12

    age_parts = []
    if years > 0:
        age_parts.append(f"{years} Year{'s' if years > 1 else ''}")
    if months > 0:
        age_parts.append(f"{months} Month{'s' if months > 1 else ''}")

    return ', '.join(age_parts) or '0 Months'