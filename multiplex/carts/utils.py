from .models import ProductCart, TicketCart


def get_user_carts(request):
    if request.user.is_authenticated:
        return ProductCart.objects.filter(user=request.user)
    if not request.session.session_key:
        request.session.create()
    return ProductCart.objects.filter(session_key=request.session.session_key)


def get_user_ticket_carts(request):
    if request.user.is_authenticated:
        return TicketCart.objects.filter(user=request.user)
    if not request.session.session_key:
        request.session.create()
    return TicketCart.objects.filter(session_key=request.session.session_key)