import pyotp
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.cache import never_cache
from administrator.models import Product, Banner
from core.forms import AddressForm
from core.models import Coupon
from core.otp import send_otp
from order.models import Order, ReturnedProduct, Wallet
from user_account.models import Address, User_profile, WishItem

# Create your views here.
@never_cache
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, "register.html")


def sign_up(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        else:
            if password_1 == password_2:
                username = email
                request.session['email'] = email
                request.session['user_data'] = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username,
                    'email': email,
                    'password': password_1
                }
                send_otp(request)
                return redirect('otp')
            else:
                messages.error(request, 'Password are not same')
                return redirect('signup')
    else:
        messages.error(request, 'Method are not allowed')


def forgot_password_action(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User with the given email does not exist.')
            return render(request, 'forgot.html')

        request.session['id'] = user_obj.id
        request.session['email'] = email
        send_otp(request)
        return redirect('forget_otp')

    return render(request, 'forgot.html')


def forget_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_key = request.session.get('otp_key')
        otp_valid = request.session.get('otp_valid')
        if otp_key and otp_valid is not None:
            valid_otp = datetime.fromisoformat(otp_valid)
            if valid_otp > datetime.now():
                totp = pyotp.TOTP(otp_key, interval=60)
                if totp.verify(otp):
                    return redirect('new_password')
                else:
                    messages.error(request, 'Invalid Otp')
                    return redirect('forget_otp')
            else:
                clear_session(request)
                messages.error(request, 'Otp expired')
                return redirect('log_in')
        else:
            clear_session(request)
            messages.error(request, 'Didnt get any otp')
            return redirect('log_in')
    return render(request, 'forgetOtp.html')


def forgot_password(request):
    return render(request, 'forgot.html')


def new_password(request):
    if request.method == 'POST':
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if password_1 == password_2:
            id = request.session.get('id')
            user = User.objects.get(id=id)
            hashed_password = make_password(password_1)
            user.password = hashed_password
            return redirect('log_in')
    return render(request, 'new_password.html')


@never_cache
def otp(request):
    if request.method == 'POST':
        user_data = request.session.get('user_data')
        otp = request.POST.get('otp')
        otp_key = request.session.get('otp_key')
        otp_valid = request.session.get('otp_valid')
        if otp_key and otp_valid is not None:
            valid_otp = datetime.fromisoformat(otp_valid)
            if valid_otp > datetime.now():
                totp = pyotp.TOTP(otp_key, interval=60)
                if totp.verify(otp):
                    User.objects.create_user(**user_data)
                    clear_session(request)
                    return redirect('login_page')
                else:
                    messages.error(request, 'Invalid Otp')
                    return redirect('otp')
            else:
                clear_session(request)
                messages.error(request, 'Otp expired')
                return redirect('signup')
        else:
            clear_session(request)
            messages.error(request, 'Didnt get any otp')
            return redirect('signup')
    return render(request, "otp.html")


@never_cache
def log_in(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admindash')
        else:
            return redirect('home')
    else:
        return render(request, "login.html")


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            if User.objects.get(username=username).is_active:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if User.objects.get(username=username).is_superuser:
                        login(request, user)
                        return redirect('admindash')
                    else:
                        login(request, user)
                        return redirect('home')
                else:
                    messages.error(request, "User doesn't find")
                    return redirect('login_page')
            else:
                messages.error(request, "User is Blocked")
                return redirect('login_page')
        else:
            messages.error(request, "User doesn't exists")
            return redirect('login_page')
    else:
        return redirect('log_in')


def log_out(request):
    request.session.flush()
    logout(request)
    return redirect('home')


def clear_session(request):
    key = ['otp_key', 'otp_valid', 'user_data', 'email']
    for key in key:
        if key in request.session:
            del request.session[key]


@never_cache
def home(request):
    if request.user.is_superuser:
        return redirect('admindash')
    product = Product.objects.exclude(Q(active=False) | Q(Brand__active=False))
    banner = Banner.objects.exclude(active=False)
    return render(request, "home_page.html", {'product': product, 'banner': banner})


def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    try:
        user_profile = User_profile.objects.get(user=request.user)
    except User_profile.DoesNotExist:
        user_profile = None
    current_date = timezone.now().date()
    coupons = Coupon.objects.filter(active=True, expiry_date__gte=current_date)
    return render(request, 'profile.html', {'user_profile': user_profile, 'orders': orders, 'coupons': coupons})


@login_required
def edit_profile(request):
    try:
        user_profile = User_profile.objects.get(user=request.user)
    except User_profile.DoesNotExist:
        user_profile = User_profile.objects.create(user=request.user)

    return render(request, 'edit profile.html', {'user_profile': user_profile})


@login_required
def edit_profileaction(request):
    user_profile = User_profile.objects.get(user=request.user)
    if request.method == 'POST':
        user = request.user
        profile_photo = request.FILES.get('photo')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        if profile_photo:
            user_profile.profile_photo = profile_photo

        user_profile.phone_number = phone_number
        user_profile.address = address

        user.name = name
        user.email = email
        user.save()

        user_profile.save()

        return redirect('profile')

    return redirect('edit_profile')


def edit_password(request):
    return render(request, 'edit_password.html')


@login_required
def set_new_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'edit_password.html', {'form': form})
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'profile.html', {'form': form})


def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.cleaned_data
            address = Address.objects.create(
                user=request.user,
                full_name=new_address['full_name'],
                address=new_address['address'],
                place=new_address['place'],
                pincode=new_address['pincode'],
                phone=new_address['phone']
            )
            return redirect('checkout')
    else:
        form = AddressForm()

    return render(request, 'add_address.html', {'form': form})


def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'address_list.html', {'addresses': addresses})


@login_required
def wallet(request):
    wallet = Wallet.objects.filter(user=request.user)
    total_balance = sum(wallet.total_balance() for wallet in wallet)
    return render(request, 'wallet.html', {'wallet': wallet, 'total_balance': total_balance})


def initiate_return(request,order_id):
    order =Order.objects.get(pk=order_id)
    existing_return = ReturnedProduct.objects.filter(order=order)
    if existing_return:
        existing_return = existing_return.get(order=order)
    else:
        if request.method == 'POST':
            reason = request.POST.get('reason')
            returned_product = ReturnedProduct.objects.create(order=order, reason=reason)
            messages.success(request,'Return initiated successfully.')
            return redirect('profile')
    return render(request, 'return_product.html',{'orders':order,'existing_return': existing_return})


def couponshow(request):
    current_date = timezone.now().date()
    coupons = Coupon.objects.filter(active=True, expiry_date__gte=current_date)
    return render(request, 'user_coupon_view.html', {'coupons':coupons})


@login_required
def wish_list(request):
    wish_items = WishItem.objects.filter(user=request.user)
    product_list = [wish_item.product for wish_item in wish_items]
    context = {
        "wish_items": wish_items,
        "products": product_list,
    }
    return render(request, 'wish.html', context)


@login_required
def add_to_wishlist(request, id):
    product = Product.objects.get(id=id)
    wish_item, created = WishItem.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f"{product.Product_name} has been added to your wishlist.")
    else:
        messages.info(request, f"{product.Product_name} is already in your wishlist.")
    default_url = '/'
    referer = request.META.get('HTTP_REFERER', default_url)
    try:
        return redirect(referer)
    except ValueError:
        return redirect(default_url)


def remove_from_wishlist(request, product_id):
    try:
        item_to_remove = WishItem.objects.get(id=product_id)
        item_to_remove.delete()
        return redirect('wishlist')
    except WishItem.DoesNotExist:
        return redirect('wishlist')


def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = Order.CANCEL
    order.save()
    order_item=order.order_items.all()
    for item in order_item:
        product = item.product
        product.Stock += item.quantity
        product.save()
    messages.success(request, 'Order successfully cancelled.')
    return redirect('profile')


def invoice(request,id):
    order = Order.objects.get(id=id)
    order_item = order.order_items.all()
    total_price = sum(item.price for item in order_item)
    return render(request,'invoice.html',{'order':order,'total_price':total_price})
