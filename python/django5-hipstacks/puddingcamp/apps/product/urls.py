from django.urls import path

from .views import partial_super_complex_pricing_api, product_list
from .views import router as router

app_name = "product"

urlpatterns = [
    path(
        "<product_id>/",
        partial_super_complex_pricing_api,
        name="partial-super-complex-pricing-api",
    ),
    path("", product_list, name="product-list"),
]
