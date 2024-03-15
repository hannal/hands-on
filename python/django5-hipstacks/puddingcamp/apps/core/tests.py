from asgiref.sync import async_to_sync
from django.test import TestCase
from django.test.client import AsyncClient
from django.urls import reverse

from apps.product.services import ProductService


class TestProductView(TestCase):
    client_class = AsyncClient

    def setUp(self) -> None:
        self.service = ProductService()
        self.products = [
            async_to_sync(self.service.create_product_with_price)("product 1", 299_792.458),
            async_to_sync(self.service.create_product_with_price)("product 2", 980_665),
        ]

    async def test_product_list(self) -> None:
        url = reverse("product:product-list")
        res = await self.client.get(url)
        assert res.status_code == 200

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
        assert res.status_code == 400

    async def test_get_product_price_htmx(self) -> None:
        url = reverse(
            "product:partial-super-complex-pricing-api",
            kwargs={"product_id": self.products[0].id},
        )
        headers = {
            "HX-REQUEST": "true",
        }
        res = await self.client.get(url, headers=headers)
        assert res.status_code == 200
