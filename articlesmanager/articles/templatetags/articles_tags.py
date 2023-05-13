from django import template

register = template.Library()


@register.simple_tag
def can_create_review(user, article):
    return user.can_create_review(article)