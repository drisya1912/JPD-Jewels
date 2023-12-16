from cart.models import CartItem
from administrator.models import Category
from user_account.models import WishItem


def category(request):
    cat = Category.objects.all().exclude(active=False)
    return {'cat':cat}


def cart(request):
    total_cart_item = 0
    if request.user.is_authenticated:
        cart = CartItem.objects.filter(user=request.user)
        for item in cart:
            total_cart_item += item.quantity
    return {'total_cart_item': total_cart_item}


def wishlist_count(request):
    if request.user.is_authenticated:
        wish = WishItem.objects.filter(user=request.user).count()
    else:
        wish = 0
    return {'wish': wish}


