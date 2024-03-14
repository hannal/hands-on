from decimal import Decimal
from typing import Sequence

from django.db import transaction

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
        with transaction.atomic():
            product = await self.repository.acreate(name=name)

            price = Decimal(price)
            await self.price_repository.acreate(product=product, price=price)
            return product

    async def get_products(self) -> Sequence[Product]:
        return [o async for o in self.repository.all()]
