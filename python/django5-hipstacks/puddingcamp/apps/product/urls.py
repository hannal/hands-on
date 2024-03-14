from django.urls import path

from .views import product_list

app_name = "product"

urlpatterns = [
    path("", product_list, name="product-list"),
]
