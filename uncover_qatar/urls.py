from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from mainApp.views import booking_success

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', admin.site.urls),
    path('api/', include('account.urls')),
    path('main-api/', include('mainApp.urls')),
    path('', include('frontend.urls')),
    path('checkout-success/', booking_success),


]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
