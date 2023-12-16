from django.urls import path
from . import views

urlpatterns = [
    path('admindash',views.admindash,name='admindash'),
    path('admcustomer',views.admcustomer, name='admcustomer'),
    path('customeraction/<int:uid>',views.customeraction, name='customeraction'),

    path('admproduct',views.admproduct,name='admproduct'),
    path('productdtl/<int:uid>',views.productdtl,name='productdtl'),
    path('delete_product/<int:uid>',views.delete_product,name='delete_product'),
    path('block_product/<int:uid>',views.block_product,name='block_product'),
    path('productadd',views.productadd,name='productadd'),
    path('productadd_perform',views.productadd_perform,name='productadd_perform'),
    path('productedit/<int:uid>',views.productedit,name='productedit'),
    path('productedit_perform',views.productedit_perform,name='productedit_perform'),

    path('categoryview',views.categoryview,name='categoryview'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('availabiltycategory/<int:uid>',views.availabiltycategory,name='availabiltycategory'),
    path('editcategory/<int:uid>',views.editcategory,name='editcategory'),
    path('editcategoryaction',views.editcategoryaction,name='editcategoryaction'),

    path('brandview',views.brandview,name='brandview'),
    path('availabilitybrand/<int:uid>',views.availabilitybrand,name='availabilitybrand'),
    path('addbrand',views.addbrand,name='addbrand'),
    path('addbrandaction',views.addbrandaction,name='addbrandaction'),
    path('brandedit/<int:uid>',views.brandedit,name='brandedit'),
    path('brandeditaction',views.brandeditaction,name='brandeditaction'),

    path('admbanner',views.admbanner,name='admbanner'),
    path('addbanner',views.addbanner,name='addbanner'),
    path('addbanner_perform',views.addbanner_perform,name='addbanner_perform'),
    path('banner_edit/<int:uid>',views.banner_edit,name='banner_edit'),
    path('banner_edit_perform',views.banner_edit_perform,name='banner_edit_perform'),
    path('banner_available/<int:uid>',views.banner_available,name='banner_available'),

    path('coupon',views.coupon, name='coupon'),
    path('edit_couponaction',views.edit_couponaction, name='edit_coupon-action'),
    path('edit_coupon/<int:id>',views.edit_coupon, name='edit_coupon'),
    path('coupon-active/<int:id>',views.couponactive,name='coupon-active'),
    path('add_coupon',views.addcoupon,name='add_coupon'),
    path('addcouponaction',views.addcouponaction,name='addcouponaction'),

    path('sales_chart/', views.sales_chart, name='sales_chart'),
    path('sales_report', views.sales_report, name='sales_report'),

    path('order',views.order,name='order'),
    path('order_details/<int:id>/', views.order_details, name='order_details'),
    path('returned_details/<int:id>/', views.returned_details, name='returned_details'),
    path('returned', views.returned, name='returned'),



    path('create_offer', views.create_offer, name='create_offer'),
    path('offers', views.offers, name='offers'),
    path('delete_offer/<int:id>', views.delete_offer, name='delete_offer'),


]