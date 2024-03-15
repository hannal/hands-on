import json

from asgiref.sync import sync_to_async
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render
from ninja import Router

from .schema import OrderCreatePayloadSchema, OrderSchema
from .services import ProductService

router = Router()


@router.post("/new-order", url_name="request-new-order", response=OrderSchema)
async def request_new_order(
    request: HttpRequest,
    payload: OrderCreatePayloadSchema,
) -> OrderSchema:
    return OrderSchema(
        order_id=1,
        product_id=payload.product_id,
        quantity=payload.quantity,
    )


async def partial_super_complex_pricing_api(
    request: HttpRequest,
    product_id: str,
) -> None:
    if not request.htmx:
        return HttpResponseBadRequest()

    service = ProductService()
    price = await service.get_optimized_price(product_id)

    ctx = {
        "price": price,
    }
    res = await sync_to_async(render)(request, "product_price.html", ctx)
    price_info = {
        "price": str(price.price),
        "productName": price.product.name,
        "type": "pyweb-symposeum-2024-optimized-price",
    }
    jsondata = {"optimizedPrice": price_info}
    res.headers["HX-Trigger"] = json.dumps(jsondata)
    return res


async def product_list(request: HttpRequest) -> None:
    service = ProductService()
    products = await service.get_products()

    ctx = {
        "products": products,
    }
    return await sync_to_async(render)(request, "product_list.jinja2", ctx)


# @sync_to_async
# def product_list(request: HttpRequest) -> None:
#     service = ProductService()
#     products = async_to_sync(service.get_products)()

#     ctx = {
#         "products": products,
#     }
#     return render(request, "product_list.html", ctx)
