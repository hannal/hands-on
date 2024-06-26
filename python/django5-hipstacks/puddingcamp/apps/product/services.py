from decimal import Decimal
from typing import Sequence

from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from libs import transaction

from .models import Price, PriceRepository, Product, ProductRepository


class ProductService:
    def __init__(
        self,
        model: Product = Product,
        repository: ProductRepository = Product.objects,
        price_repository: PriceRepository = Price.objects,
    ) -> None:
        self.model = model
        self.repository = repository
        self.price_repository = price_repository

    async def create_product_with_price(self, name: str, price: int | float) -> Product:
        async with transaction.aatomic():
            product = await self.repository.acreate(name=name)

            price = Decimal(price)
            await self.price_repository.acreate(product=product, price=price)
            return product

    async def get_products(self) -> Sequence[Product]:
        # qs = self.repository.prefetch_related("price_set")
        qs = self.repository
        return [o async for o in qs.all()]

    async def get_optimized_price(self, product_id: int | str) -> Price:
        qs = self.price_repository
        qs = qs.select_related("product")
        qs = qs.filter(product_id=product_id)
        return await qs.afirst()

    async def get_product_by_id(self, product_id: str | int) -> Product:
        # return get_object_or_404(self.repository, pk=product_id)
        return await sync_to_async(get_object_or_404)(self.repository, pk=product_id)
