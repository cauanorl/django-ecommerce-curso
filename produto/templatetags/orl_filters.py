from django import template
from utils import utils


register = template.Library()

@register.filter(name='cash_filter')
def cash_filter(cash):
    return utils.cash_filter(cash)


@register.filter(name='sum_quantity')
def sum_quantity(cart):
    return utils.sum_quantity(cart)


@register.filter(name='sum_total')
def sum_total(cart):
    return utils.sum_total(cart)