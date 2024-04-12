from django import template


from carts.utils import get_user_carts, get_user_ticket_carts

register = template.Library()


@register.simple_tag()
def user_product_carts(request):
    return get_user_carts(request)


@register.simple_tag()
def user_ticket_carts(request):
    return get_user_ticket_carts(request)
