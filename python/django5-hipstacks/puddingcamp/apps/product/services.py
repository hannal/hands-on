from decimal import Decimal
from typing import Sequence

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
        qs = self.repository.prefetch_related("price_set")
        return [o async for o in qs.all()]
