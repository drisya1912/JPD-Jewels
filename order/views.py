import uuid
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from administrator.models import Product
from cart.models import CartItem
from order.models import OrderItem, Order, Wallet
from user_account.models import Address, Applied_coupon


# Create your views here.
def checkout(request):
    address = Address.objects.filter(user=request.user)
    total_price = request.session.get('total_price')
    discount_price = request.session.get('discount_price')
    form = ''
    cart = CartItem.objects.filter(user=request.user)
    host = request.get_host()
    if not cart:
        messages.error(request, 'Your cart is empty. Please add items before placing an order.')
        return redirect('cart')
    if request.method == 'POST':
        address = request.POST.get('address')
        addr = Address.objects.get(id=address)
        payment_method = request.POST.get('payment_method')
        total_price = request.session.get('total_price')

        if payment_method == 'COD':
            order = Order.objects.create(
                user=request.user,
                address_id=address,
                total_paid=total_price,
                billing_status=payment_method
            )

            for item in cart:
                product = item.product
                price = item.total_price()
                quantity = item.quantity

                OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
                pro = Product.objects.get(id=product.id)
                pro.Stock -= quantity
                pro.save()
            cart.delete()
            coupon = request.session.get('coupon')
            Applied_coupon.objects.create(user=request.user, coupon=coupon)
            del request.session['coupon']
            del request.session['total_price']
            del request.session['discount_price']
            return redirect('profile')

        elif payment_method == 'Wallet':
            user = request.user
            wallets = Wallet.objects.filter(user=user)
            wallet_balance = sum(wallet.total_balance() for wallet in wallets)

            if wallet_balance > total_price:
                coupon = request.session.get('coupon')
                order =Order.objects.create(user=user, address_id=address, paid=True, total_paid=total_price, billing_status=payment_method)
                Applied_coupon.objects.create(user=user, coupon=coupon)
                Wallet.objects.create(user=user, amount=order.total_paid, balance_type=Wallet.DEBIT)

                for item in cart:
                    product = item.product
                    price = item.total_price()
                    quantity = item.quantity

                    OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
                    pro = Product.objects.get(id=product.id)
                    pro.Stock -= quantity
                    pro.save()
                cart.delete()
                coupon = request.session.get('coupon')
                Applied_coupon.objects.create(user=request.user, coupon=coupon)
                del request.session['coupon']
                del request.session['total_price']
                del request.session['discount_price']
                return redirect('profile')

        else:
            items = []
            for item in cart:
                product = item.product
                price = item.total_price()
                quantity = item.quantity

                item_dict = {
                    'product': product,
                    'quantity': quantity,
                    'price': price,
                }
                items.append(item_dict)

            paypal_dict = {
                "business": 'dichu01@gmail.com',
                "amount": total_price,
                "currency_code": "USD",
                "item_name": items,
                "invoice": uuid.uuid4(),
                "notify_url": f"http://{host}{(reverse('paypal-ipn'))}",
                "return": f"http://{host}{(reverse('paypal_success', kwargs={'address': address}))}",
                "cancel_return": f"http://{host}{(reverse('paypal_error'))}",
            }

            # Create the instance.
            form = PayPalPaymentsForm(initial=paypal_dict)
            context = {
                "form": form,
                'addr': addr,
                'total_price': total_price,
                'discount_price': discount_price,
            }
            return render(request, "checkout.html", context)

    context = {
        'address': address,
        'total_price': total_price,
        'discount_price': discount_price,
        "form": form
    }
    return render(request, 'checkout.html', context)


def paypal_error(request):
    return HttpResponse("Payment failed or canceled. Please try again.")


def paypal_success(request, address):
    total_price = request.session.get('total_price')
    coupon = request.session.get('coupon')
    cart = CartItem.objects.filter(user=request.user)
    Applied_coupon.objects.create(user=request.user, coupon=coupon)
    order = Order.objects.create(
        user=request.user,
        address_id=address,
        total_paid=total_price,
        billing_status='PayPal',
        paid=True
    )

    for item in cart:
        product = item.product.id
        price = item.total_price()
        quantity = item.quantity

        OrderItem.objects.create(order=order, product_id=product, price=price, quantity=quantity)

        pro = Product.objects.get(id=product)
        pro.Stock -= quantity
        pro.save()
    cart.delete()
    coupon = request.session.get('coupon')
    Applied_coupon.objects.create(user=request.user, coupon=coupon)
    del request.session['coupon']
    del request.session['total_price']
    del request.session['discount_price']
    return redirect('profile')


def payment_details(request,id):
    order = Order.objects.get(id=id)
    return render(request, 'place_order.html',  {'order': order})