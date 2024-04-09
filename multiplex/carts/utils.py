from .models import ProductCart


def get_user_carts(request):
    if request.user.is_authenticated:
        return ProductCart.objects.filter(user=request.user)
    if not request.session.session_key:
        request.session.create()
    return ProductCart.objects.filter(session_key=request.session.session_key)