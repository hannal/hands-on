from injector import Binder, InstanceProvider, Module, inject, provider, singleton

from .models import Price, PriceRepository, Product, ProductRepository
from .services import ProductService


class ProductContainer(Module):
    def configure(self, binder: Binder) -> Binder:
        binder.bind(ProductRepository, to=InstanceProvider(Product.objects), scope=singleton)
        binder.bind(PriceRepository, to=InstanceProvider(Price.objects), scope=singleton)

    @provider
    @inject
    def provide_product_service(
        self,
        product_repository: ProductRepository,
        price_repository: PriceRepository,
    ) -> ProductService:
        return ProductService(Product, product_repository, price_repository)
