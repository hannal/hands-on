from django.db import models


class ProductRepository(models.QuerySet):
    pass


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductRepository.as_manager()

    def __str__(self):
        return self.name


class PriceRepository(models.QuerySet):
    pass


class Price(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PriceRepository.as_manager()

    def __str__(self):
        return f'{self.product_id} - {self.price}'
