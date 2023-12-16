from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:id>/<str:action>/', views.update_cart, name='update_cart'),
]