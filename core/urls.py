from django.urls import path
from . import views


urlpatterns = [
    path('productview/<int:uid>',views.productview,name='productview'),
    path('collection',views.collection,name='collection'),
    path('search',views.search,name='search'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('price_filter',views.price_filter,name='price_filter'),
    path('banner',views.banner,name='banner'),
    # path('calculate_discounted_price',views.calculate_discounted_price,name='calculate_discounted_price'),
]
