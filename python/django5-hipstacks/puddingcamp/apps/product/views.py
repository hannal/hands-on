from asgiref.sync import sync_to_async
from django.http import HttpRequest
from django.shortcuts import render

from .services import ProductService


async def product_list(request: HttpRequest) -> None:
    service = ProductService()
    products = await service.get_products()

    ctx = {
        "products": products,
    }
    return await sync_to_async(render, thread_sensitive=True)(request, "product_list.html", ctx)
