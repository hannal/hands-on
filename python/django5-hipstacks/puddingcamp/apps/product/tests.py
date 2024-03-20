import json
from http import HTTPStatus

from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import AsyncClient
from django.urls import reverse

from apps.product.schema import OrderSchema
from apps.product.services import ProductService


class TestProductView(TestCase):
    client_class = AsyncClient

    def setUp(self) -> None:
        self.service = ProductService()
        self.products = [
            async_to_sync(self.service.create_product_with_price)("product 1", 299_792.458),
            async_to_sync(self.service.create_product_with_price)("product 2", 980_665),
        ]
        self.user = User.objects.create_user("test", "")

    async def test_product_list(self) -> None:
        url = reverse("product:product-list")
        res = await self.client.get(url)
        assert res.status_code == HTTPStatus.OK

        # self.assertContains(res, "가격 :", html=False)
        # for product in self.products:
        #     async for price in product.price_set.all():
        #         self.assertContains(res, f"가격 : {price.price}", html=True)

    async def test_get_product_price_without_htmx(self) -> None:
        url = reverse(
            "product:partial-super-complex-pricing-api",
            kwargs={"product_id": self.products[0].id},
        )
        res = await self.client.get(url)
        assert res.status_code == HTTPStatus.BAD_REQUEST

    async def test_get_product_price_htmx(self) -> None:
        product = self.products[0]
        url = reverse(
            "product:partial-super-complex-pricing-api",
            kwargs={"product_id": product.id},
        )
        headers = {
            "HX-REQUEST": "true",
        }
        res = await self.client.get(url, headers=headers)
        if htmx_data := res.headers.get("HX-Trigger"):
            data = json.loads(htmx_data)
            assert "optimizedPrice" in data
            data = data["optimizedPrice"]

            assert "price" in data
            assert data["productName"] == product.name
            assert "type" in data
        assert res.status_code == HTTPStatus.OK

    async def test_request_new_order(self) -> None:
        product = self.products[0]
        url = reverse("ninja:request-new-order")
        headers = {"HX-REQUEST": "true"}
        payload = {
            "product_id": product.id,
            "quantity": 1,
        }
        res = await self.client.post(
            url,
            data=payload,
            content_type="application/json",
            headers=headers,
        )

        assert res.status_code == HTTPStatus.OK
        data = OrderSchema.model_validate(res.json())
        assert isinstance(data.order_id, int)
        assert data.product_id == payload["product_id"]
        assert data.quantity == payload["quantity"]

    async def test_anonymous_cannot_set_favorite(self) -> None:
        product = self.products[0]
        url = reverse("ninja:set-favorite-api", kwargs={"product_id": product.id})
        res = await self.client.post(url)
        assert res.status_code == HTTPStatus.FORBIDDEN

    async def test_set_favorite(self) -> None:
        product = self.products[0]
        url = reverse("ninja:set-favorite-api", kwargs={"product_id": product.id})
        await self.client.aforce_login(self.user)
        res = await self.client.post(url)
        assert res.status_code == HTTPStatus.OK
