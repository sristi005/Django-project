# core/context_processors.py  (new file)
from core.auth_utils import get_logged_in_user
from core.models import Cart

def cart_context(request):
    user = get_logged_in_user(request)
    if user:
        cart = Cart.objects.filter(user=user).first()
        if cart:
            return {"cart_count": cart.total_items()}
    return {"cart_count": 0}