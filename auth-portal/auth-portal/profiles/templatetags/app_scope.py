from django import template

register = template.Library()


@register.simple_tag
def get_scope(app_obj):
    scope = app_obj.scope
    allowed_scope = [scope.choices[elem] for elem in scope]
    return allowed_scope
