from django import template

register = template.Library()

@register.filter
def total(incomes):
    total = 0
    for income in incomes:
        total = total + income.income
    return total