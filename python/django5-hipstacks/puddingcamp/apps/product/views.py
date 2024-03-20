import json

from asgiref.sync import sync_to_async
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render
from ninja_extra import (
    ControllerBase,
    Router,
    api_controller,
    http_delete,
    http_get,
    http_post,
    permissions,
)

from .schema import OrderCreatePayloadSchema, OrderSchema, ProductSchema
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


@api_controller("/favorites", permissions=[permissions.IsAuthenticated])
class FavoriteController(ControllerBase):
    def __init__(self, product_service: ProductService) -> None:
        self.product_service = product_service

    @http_post("/{product_id}", url_name="set-favorite-api")
    async def set_favorite(
        self,
        request: HttpRequest,
        product_id: int,
    ) -> ProductSchema:
        product = await self.product_service.get_product_by_id(product_id)
        return ProductSchema.model_validate(product)

    @http_delete("/{product_id}", url_name="unset-favorite-api")
    async def unset_favorite(
        self,
        request: HttpRequest,
        product_id: int,
    ) -> None:
        product = await self.product_service.get_product_by_id(product_id)
        return ProductSchema.model_validate(product)

    @http_get("", url_name="favorites-api")
    async def favorites(self, request: HttpRequest) -> None:
        products = await self.product_service.get_products()
        return [ProductSchema.model_validate(product) for product in products]


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
        "is_partial": bool(request.htmx),
    }
    res = await sync_to_async(render)(request, "product_price.jinja2", ctx)
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
