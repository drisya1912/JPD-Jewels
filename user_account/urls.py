from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('signup',views.signup,name='signup'),
    path('sign_up',views.sign_up,name='sign_up'),
    path('log_in',views.log_in,name='log_in'),
    path('login_page',views.login_page,name='login_page'),
    path('otp',views.otp,name='otp'),
    path('log_out',views.log_out,name='log_out'),

    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('forgot_password_action', views.forgot_password_action, name='forgot_password_action'),
    path('forget_otp', views.forget_otp, name='forget_otp'),
    path('new_password',views.new_password, name='new_password'),
    path('profile',views.profile,name='profile'),
    path('edit_profile', views.edit_profile,name='edit_profile'),
    path('edit_profileaction', views.edit_profileaction,name='edit_profileaction'),
    path('edit_password',views.edit_password,name='edit_password'),
    path('set_new_password/', views.set_new_password, name='set_new_password'),

    path('add_address/', views.add_address, name='add_address'),
    path('address_list/', views.address_list, name='address_list'),
    path('initiate_return/<int:order_id>',views.initiate_return,name='initiate_return'),
    path('wallet',views.wallet,name='wallet'),
    path('couponshow',views.couponshow,name='couponshow'),
    path('wishlist', views.wish_list, name='wishlist'),
    path('addtowishlist/<int:id>', views.add_to_wishlist, name='addtowishlist'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('invoice/<int:id>',views.invoice,name='invoice'),

]