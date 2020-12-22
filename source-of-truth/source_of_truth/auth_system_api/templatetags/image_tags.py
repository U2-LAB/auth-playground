from django import template
from libgravatar import Gravatar

register = template.Library()

@register.simple_tag
def get_gravatar_url(email):
    g = Gravatar(email)
    return g.get_image(default='identicon')