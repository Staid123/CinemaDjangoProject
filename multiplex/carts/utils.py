from .models import ProductCart


def get_user_carts(request):
    if request.user.is_authenticated:
        return ProductCart.objects.filter(user=request.user)