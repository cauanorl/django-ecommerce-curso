from django.contrib import admin
from .models import Product, Variation


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1


class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'name', 'get_formated_price',
        'get_formated_promotional_price', 'type_product')
    list_display_links = ('id', 'name')

    inlines = [
        VariationInline,
    ]

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
