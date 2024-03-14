from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import urlpatterns as staticfiles_urlpatterns

urlpatterns = [
    path('products/', include('apps.product.urls')),
    path('admin/', admin.site.urls),
]
urlpatterns.extend(staticfiles_urlpatterns)

