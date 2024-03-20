from django.contrib import admin

from .models import Product, Price


class PriceInline(admin.TabularInline):
    model = Price
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInline]
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

