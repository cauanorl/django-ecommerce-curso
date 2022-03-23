from django import template
from utils import utils


register = template.Library()

@register.filter(name='cash_filter')
def cash_filter(cash):
    return utils.cash_filter(cash)
