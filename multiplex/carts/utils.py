from .models import ProductCart, TicketCart


def get_user_carts(request):
    if request.user.is_authenticated:
        return ProductCart.objects.filter(user=request.user).select_related('product')
    if not request.session.session_key:
        request.session.create()
    return ProductCart.objects.filter(session_key=request.session.session_key).select_related('product')


def get_user_ticket_carts(request):
    if request.user.is_authenticated:
        return TicketCart.objects.filter(user=request.user).select_related('ticket')
    if not request.session.session_key:
        request.session.create()
    return TicketCart.objects.filter(session_key=request.session.session_key).select_related('ticket')