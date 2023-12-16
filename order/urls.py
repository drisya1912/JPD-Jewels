from django.urls import path
from . import views


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('paypal_error', views.paypal_error, name='paypal_error'),
    path('paypal_success/<int:address>', views.paypal_success, name='paypal_success'),
    path('payment_details/<int:id>', views.payment_details, name='payment_details'),
]