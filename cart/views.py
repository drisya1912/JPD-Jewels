from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from administrator.models import Product
from cart.models import CartItem
from core.forms import CouponForm
from core.models import Coupon
from user_account.models import Applied_coupon, WishItem


# Create your views here.
@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    if CartItem.objects.filter(user=request.user, product_id=id).exists():
        messages.info(request, f"{product.Product_name} is already in your cart.")
        default_url = '/'
        referer = request.META.get('HTTP_REFERER', default_url)
        try:
            return redirect(referer)
        except ValueError:
            return redirect(default_url)
    else:
        wish = WishItem.objects.filter(product=product)
        item = CartItem.objects.create(product=product, quantity=1)
        if request.user:
            item.user = request.user
            item.save()
            messages.success(request, f"{product.Product_name} has been added to your cart.")
        if wish.exists():
            for item in wish:
                item.delete()
        default_url = '/'
        referer = request.META.get('HTTP_REFERER', default_url)
        try:
            return redirect(referer)
        except ValueError:
            return redirect(default_url)


@login_required
def cart(request):
    cart = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart)
    cart_total_price = sum(item.total_price() for item in cart)
    discount_price = int(0)
    coupon_form = CouponForm(request.POST)
    code = ""
    coupon = ""

    if coupon_form.is_valid():
        code = coupon_form.cleaned_data['code']
        coupon = Coupon.objects.filter(code=code, active=True)
        if Applied_coupon.objects.filter(user=request.user, coupon=code).exists():
            messages.error(request, f"The Coupon {code} is Already used before")
        else:
            try:
                coupon = Coupon.objects.get(code=code, expiry_date__gte=timezone.now(), active=True)
                if total_price < coupon.discount:
                    messages.error(request, "invalid coupon")
                    return redirect('cart')
                total_price -= coupon.discount
                discount_price = coupon.discount
                messages.success(request, f'Coupon {code} applied successfully!')
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid coupon code.')

    request.session['coupon'] = code
    request.session['total_price'] = int(total_price)
    request.session['discount_price'] = discount_price
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price, 'coupon_form': coupon_form, 'coupon': coupon, 'cart_total_price': cart_total_price, 'discount_price': discount_price})


def update_cart(request, id, action):
    cart = get_object_or_404(CartItem, product=id, user=request.user)
    product = cart.product

    if action == 'increment':
        cart.quantity += 1
    elif action == 'decrement':
        cart.quantity -= 1

    cart.save()
    if cart.quantity == 0:
        cart.delete()

    default_url = '/'
    referer = request.META.get('HTTP_REFERER', default_url)

    try:
        return redirect(referer)
    except ValueError:
        return redirect(default_url)
