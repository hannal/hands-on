from django.contrib import admin
from django.contrib.staticfiles.urls import urlpatterns as staticfiles_urlpatterns
from django.urls import include, path
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router("products", "apps.product.urls.router")

urlpatterns = [
    path("products/", include("apps.product.urls")),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
urlpatterns.extend(staticfiles_urlpatterns)
