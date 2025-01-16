from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_rooot=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_rooot=settings.MEDIA_ROOT)
