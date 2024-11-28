from django import template
from django.core.signing import Signer

register = template.Library()

@register.filter
def sign_id(id):
    signer = Signer()
    return signer.sign(id)
