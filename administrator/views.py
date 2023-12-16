from datetime import timedelta, datetime
from django.contrib import messages
from django.db.models import Count, Case, When, IntegerField
from django.db.models.functions import ExtractMonth
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.cache import never_cache
from administrator.models import *
from core.forms import OfferForm
from core.models import *
from django.http import JsonResponse
from order.models import OrderItem, Order, ReturnedProduct, Wallet


# Create your views here.
@never_cache
def admindash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        customers = User.objects.exclude(is_superuser=True)
        products = Product.objects.all()
        categories = Category.objects.all()
        brands = Brand.objects.all()
        orders = Order.objects.all()
        coupons = Coupon.objects.all()
        context = {
            'customers': customers,
            'products': products,
            'categories': categories,
            'brands': brands,
            'orders': orders,
            'coupons': coupons,
        }
        return render(request, "adm/database.html", context)
    else:
        return redirect('home')


def admcustomer(request):
    customer = User.objects.all().exclude(is_superuser=True)
    return render(request, "adm/customer.html", {'customer': customer})


def customeraction(request, uid):
    customer = User.objects.get(id=uid)
    if customer.is_active:
        customer.is_active = False
    else:
        customer.is_active = True
    customer.save()
    return redirect('admcustomer')


def admproduct(request):
    product = Product.objects.all()
    return render(request, "adm/product.html", {'product': product})


def productdtl(request, uid):
    product = Product.objects.get(id=uid)
    return render(request, "adm/product_view.html", {'product': product})


def delete_product(request, uid):
    if request.method == 'POST':
        product = Product.objects.get(id=uid)
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('admproduct')


def block_product(request, uid):
    product = Product.objects.get(id=uid)
    if product.active:
        product.active = False
    else:
        product.active = True
    product.save()
    return redirect('admproduct')


def productadd(request):
    brand = Brand.objects.exclude(active=False)
    category = Category.objects.exclude(active=False)
    context = {
        'brand': brand,
        'category': category
    }
    return render(request, 'adm/product_add.html', context)


def productadd_perform(request):
    if request.method == 'POST':
        name = request.POST.get('pname')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        stock = request.POST.get('stock')
        price = request.POST.get('price')

        if price and price.replace('.', '', 1).isdigit():
            if float(price) < 0:
                messages.error(request, "Price cannot be negative.")
                return redirect('admproduct')
        else:
            messages.error(request, "Invalid price value.")
            return redirect('productadd')

        if stock and stock.replace('.', '', 1).isdigit():
            if float(stock) < 0:
                messages.error(request, "Stock cannot be negative.")
                return redirect('admproduct')
        else:
            messages.error(request, "Invalid stock value.")
            return redirect('productadd')

        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')

        product = Product(Product_name=name, Brand_id=brand, Category_id=category, price=price, Stock=stock,
                          Description=description, img1=img1, img2=img2, img3=img3, img4=img4)
        product.save()
        return redirect('admproduct')
    else:
        return redirect('admproduct')


def productedit(request, uid):
    product = Product.objects.get(id=uid)
    brand = Brand.objects.exclude(active=False)
    category = Category.objects.exclude(active=False)
    context = {
        'product': product,
        'brand': brand,
        'category': category
    }
    return render(request, 'adm/product_edit.html', context)


def productedit_perform(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('pname')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        stock = request.POST.get('stock')
        if stock and stock.replace('.', '', 1).isdigit():
            if float(stock) < 0:
                messages.error(request, "stoke cannot be negative.")
                return redirect('productedit', uid=id)
        else:
            messages.error(request, "Invalid stoke value.")
            return redirect('productedit', uid=id)

        price = request.POST.get('price')
        if price and price.replace('.', '', 1).isdigit():
            if float(price) < 0:
                messages.error(request, "Price cannot be negative.")
                return redirect('productedit', uid=id)
        else:
            messages.error(request, "Invalid price value.")
            return redirect('productedit', uid=id)
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')

        product = Product.objects.get(id=id)

        product.Product_name = name
        product.Brand_id = brand
        product.Category_id = category
        product.price = price
        product.Stock = stock
        product.Description = description

        if img1 is not None:
            product.img1 = img1
        if img2 is not None:
            product.img2 = img2
        if img3 is not None:
            product.img3 = img3
        if img4 is not None:
            product.img4 = img4

        product.save()
        return redirect('admproduct')
    else:
        return redirect('admproduct')


def admbanner(request):
    banner = Banner.objects.all()
    return render(request, 'adm/banner.html', {'banner': banner})


def addbanner(request):
    return render(request, 'adm/banneradd.html')


def addbanner_perform(request):
    if request.method == 'POST':
        name = request.POST.get('bname')
        # description = request.POST.get('description')
        img1 = request.FILES.get('img1')

        banner = Banner(banner_name=name, img1=img1)
        banner.save()
        return redirect('admbanner')
    else:
        return redirect('admbanner')


def banner_edit(request, uid):
    banner = Banner.objects.get(id=uid)
    return render(request, 'adm/banner_edit.html', {'banner': banner})


def banner_edit_perform(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('bname')

        img1 = request.FILES.get('img1')

        banner = Banner.objects.get(id=id)

        banner.banner_name = name

        if img1 is not None:
            banner.img1 = img1

        banner.save()
        return redirect('admbanner')
    else:
        return redirect('admbanner')


def banner_available(request,uid):
    banner = Banner.objects.get(id=uid)
    if banner.active:
        banner.active = False
    else:
        banner.active = True
    banner.save()
    return redirect('admbanner')


def categoryview(request):
    cat = Category.objects.all()
    return render(request, 'adm/category.html', {'cat': cat})


def addcategory(request):
    if request.method == 'POST':
        name = request.POST.get('cat')
        if Category.objects.filter(name=name).exists():
            messages.error(request, f"A category with the name '{name}' already exists.")
            return redirect('addcategory')
        Category.objects.create(name=name)
        return redirect('categoryview')

    return render(request, 'adm/add_category.html')


def availabiltycategory(request, uid):
    category = Category.objects.get(id=uid)
    if category.active:
        category.active = False
    else:
        category.active = True
    category.save()
    return redirect('categoryview')


def editcategory(request, uid):
    category = Category.objects.get(id=uid)
    return render(request, 'adm/editcategory.html', {'category': category})


def editcategoryaction(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('cat')
        if Category.objects.filter(name=name).exclude(id=id).exists():
            messages.error(request, f"A category with the name '{name}' already exists.")
            return redirect('editcategory', uid=id)
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return redirect('categoryview')


def brandview(request):
    brand = Brand.objects.all()
    return render(request, 'adm/brandview.html', {'brand': brand})


def availabilitybrand(request, uid):
    brand = Brand.objects.get(id=uid)
    if brand.active:
        brand.active = False
    else:
        brand.active = True
    brand.save()
    return redirect('brandview')


def addbrand(request):
    return render(request, 'adm/addbrand.html')


def addbrandaction(request):
    if request.method == 'POST':
        name = request.POST.get('brand')
        if Brand.objects.filter(name=name).exists():
            messages.error(request, f"A brand with the name '{name}' already exists.")
            return redirect('addbrand')

        Brand.objects.create(name=name)
        return redirect('brandview')


def brandedit(request, uid):
    brand = Brand.objects.get(id=uid)

    return render(request, 'adm/brandedit.html', {'brand': brand})


def brandeditaction(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('brand')

        if Brand.objects.filter(name=name).exclude(id=id).exists():
            messages.error(request, f"A brand with the name '{name}' already exists.")
            return redirect('brandedit', uid=id)

        brand = Brand.objects.get(id=id)
        brand.name = name
        brand.save()
        return redirect('brandview')


def coupon(request):
    coupon = Coupon.objects.all()
    return render(request, 'adm/coupon.html', {'coupon': coupon})


def addcoupon(request):
    return render(request, 'adm/admin_add_coupon.html')


def addcouponaction(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        # valid_from = request.POST.get('valid_from')
        valid_to_str = request.POST.get('valid_to')
        discount = request.POST.get('discount_amount')

        expiry_date = datetime.strptime(valid_to_str, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')

        Coupon.objects.create(code=code, expiry_date=expiry_date, discount=discount)
        return redirect('coupon')
    else:
        return redirect('add_coupon')


def edit_coupon(request, id):
    coupon = Coupon.objects.get(id=id)
    return render(request, 'adm/edit_coupon.html', {'coupon': coupon})


def edit_couponaction(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        code = request.POST.get('code')
        valid_to_str = request.POST.get('valid_to')
        discount = request.POST.get('discount_amount')

        coupon = Coupon.objects.get(id=id)
        coupon.code = code
        coupon.discount = discount

        if valid_to_str:
            expiry_date = datetime.strptime(valid_to_str, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
            coupon.expiry_date = expiry_date

        coupon.save()
        return redirect('coupon')

    return render(request, 'adm/coupon.html')


def couponactive(request, id):
    coupon = Coupon.objects.get(id=id)
    current_date = timezone.now().date()
    if coupon.active:
        coupon.active = False
    else:
        coupon.active = True
    coupon.save()
    return redirect('coupon')


def sales_report(request):
    orders = Order.objects.filter(status='delivered')
    total_sales = sum(order.total_paid for order in orders)
    order_items = OrderItem.objects.filter(order__in=orders)
    total_quantity_sold = sum(item.quantity for item in order_items)

    context = {
        'total_sales': total_sales,
        'total_quantity_sold': total_quantity_sold,
        'orders': orders,
    }
    return render(request, 'adm/sales_report.html', context)

def order(request):
    order = Order.objects.all()
    return render(request, 'adm/order.html', {'order': order})


def returned(request):
    returned = ReturnedProduct.objects.all()
    return render(request, 'adm/return.html' ,{'returned':returned})


def returned_details(request, id):
    returned = ReturnedProduct.objects.get(id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            returned.return_status = new_status
            order = returned.order
            if new_status == returned.RETURNED:
                order.status = order.RETURNED
                order.save()

                order_item = order.order_items.all()
                for item in order_item:
                    product = item.product
                    product.Stock += item.quantity
                    product.save()

                Wallet.objects.create(user=order.user, amount=order.total_paid, order=order)
            returned.save()
            return redirect('returned_details', id=id)
    return render(request, "adm/return_view.html", {'returned': returned})


def order_details(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status
            order.save()
            return redirect('order_details', id=id)
    return render(request, "adm/order_view.html", {'order': order})


def sales_chart(request):
    sales_data = Order.objects.annotate(
        month=ExtractMonth('created')
    ).values('month').annotate(
        total_sales=Count(Case(When(status='Delivered', then=1), output_field=IntegerField())),
        total_canceled=Count(Case(When(status='Cancelled', then=1), output_field=IntegerField())),
    )

    labels = [str(data['month']) for data in sales_data]
    sales_values = [data['total_sales'] for data in sales_data]
    canceled_values = [data['total_canceled'] for data in sales_data]

    chart_data = {'labels': labels, 'sales_values': sales_values, 'canceled_values': canceled_values}

    return render(request, 'adm/sales_chart.html', {'chart_data': chart_data})



def create_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            offer = Offer.objects.filter(product=product)
            if offer:
                discount_type = form.cleaned_data['discount_type']
                discount_value = form.cleaned_data['discount_value']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                offer = Offer.objects.get(product=product)
                offer.discount_type = discount_type
                offer.discount_value = discount_value
                offer.start_date = start_date
                offer.end_date = end_date
                offer.save()
            else:
                form.save()
            return redirect('offers')
    else:
        form = OfferForm()

    return render(request, 'adm/addOffer.html', {'form': form})


def offers(request):
    offers = Offer.objects.all()
    return render(request, 'adm/offers.html', {'offers': offers})


def delete_offer(request, id):
    Offer.objects.get(pk=id).delete()
    return redirect('offers')