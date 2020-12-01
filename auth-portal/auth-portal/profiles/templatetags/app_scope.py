from django import template
from users.models import MyApplication

register = template.Library()

@register.simple_tag
def get_scope(app_obj):
    scope = app_obj.scope
    print(scope.choices)
    allowed_scope = [scope.choices[elem] for elem in scope]
    print(allowed_scope)
    return allowed_scope