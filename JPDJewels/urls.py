from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include("administrator.urls")),
    path('', include("core.urls")),
    path('', include("cart.urls")),
    path('', include("order.urls")),
    path('', include("user_account.urls")),

    path('main_admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('paypal/', include("paypal.standard.ipn.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
