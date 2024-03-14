from django.http import HttpRequest
from django.shortcuts import render

from .services import ProductService


async def product_list(request: HttpRequest) -> None:
    service = ProductService()
    products = await service.get_products()

    ctx = {
        "products": products,
    }

    return render(request, "product_list.html", ctx)
