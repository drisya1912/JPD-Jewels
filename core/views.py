from django.db.models import Q
from django.shortcuts import render
from django.contrib import messages
from administrator.models import *
from django.http import JsonResponse

# Create your views here.
def productview(request, uid):
    product = Product.objects.get(id=uid)
    offer = Offer.objects.filter(product_id=uid, start_date__lte=timezone.now(), end_date__gte=timezone.now()).first()
    # if offer:
    #     offer = offer.get(product_id=uid)
    discounted_price = product.get_discounted_price()
    return render(request, 'productview.html', {'product': product, 'offer': offer, 'discounted_price': discounted_price})



def banner(request):
    banner = Banner.objects.all()
    return render(request, 'home_page.html', {'banner':banner})


def banner(request, uid):
    banner = Banner.objects.get(id=uid)
    return render(request, 'adm/banner_edit.html')

def collection(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    product = Product.objects.all().exclude(Q(active=False) | Q(Brand__active=False))

    active_category = request.GET.get('category', '')
    active_brand = request.GET.get('brand', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    product_filter = Q()

    if active_category:
        product_filter &= Q(Category__id=active_category)

    if active_brand:
        product_filter &= Q(Brand__id=active_brand)

    if min_price and max_price:
        product_filter &= Q(price__gte=min_price, price__lte=max_price)

    # Apply the filter to the products
    product = product.filter(product_filter)
    offer = Offer.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).first()

    for prod in product:
        if offer:
            discounted_price = prod.get_discounted_price()
            setattr(prod, 'discounted_price', discounted_price)

    context = {
        'category': category,
        'product': product,
        'brand': brand,
        'active_category': active_category,
        'active_brand': active_brand,
        'min_price': min_price,
        'max_price': max_price,
        'offer': offer,
    }
    return render(request, 'collection.html', context)


def search(request):
    query = request.GET.get('query')
    if query:
        products = Product.objects.filter(Product_name__icontains=query).exclude(active=False)
        if products.exists():
            return render(request, 'collection.html', {'product': products})
        else:
            messages.warning(request, f'No products found for "{query}". Try searching for something else.')
    else:
        messages.info(request, 'Please enter a search query.')
    return render(request, 'collection.html')


def search_suggestions(request):
    query = request.GET.get('term', '')
    results = Product.objects.filter(Q(Product_name__icontains=query) & Q(active=True))[:10]
    suggestions = [{'value': product.Product_name} for product in results]
    return JsonResponse(suggestions, safe=False)


def price_filter(request):
    product = Product.objects.none()

    if request.method == "POST":
        min_price = request.POST.get("min_price")
        max_price = request.POST.get("max_price")

        if min_price and max_price:
            try:
                min_price = float(min_price)
                max_price = float(max_price)

                if max_price < min_price:
                    error_message = "Maximum price should be greater than or equal to the minimum price."
                    return render(request, "collection.html", {'error_message': error_message})

            except ValueError:
                error_message = "Invalid price values"
                return render(request, "collection.html", {'error_message': error_message})

            # Filter products based on price range
            product = Product.objects.filter(
                Q(price__gte=min_price) & Q(price__lte=max_price)).exclude(active=False)

    return render(request, "collection.html", {"product": product})
