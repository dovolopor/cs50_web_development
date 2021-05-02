from django import template

minInrementInCents = 1

register = template.Library()

@register.filter
def toMoney(value):
    doll = value // 100
    cent = value % 100
    centStr = cent if cent > 9 else f'0{cent}'
    return f"{doll}.{centStr}"

@register.filter
def toNextValMoney(value):
    value += minInrementInCents
    doll = value // 100
    cent = value % 100
    centStr = cent if cent > 9 else f'0{cent}'
    return f"{doll}.{centStr}"