from apps.product.views import FavoriteController
from django.contrib import admin
from django.contrib.staticfiles.urls import urlpatterns as staticfiles_urlpatterns
from django.urls import include, path
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

api.add_router("products", "apps.product.urls.router")
api.register_controllers(
    FavoriteController,
)

urlpatterns = [
    path("products/", include("apps.product.urls")),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
urlpatterns.extend(staticfiles_urlpatterns)
