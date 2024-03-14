from django.http import HttpRequest
from django.shortcuts import render


async def product_list(request: HttpRequest) -> None:
    return render(request, "product_list.html", {})
