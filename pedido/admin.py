from django.contrib import admin

from .models import Purchase, PurchaseItem


class PurchaseItensInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1


class PurchaseAdmin(admin.ModelAdmin):
    inlines = [
        PurchaseItensInline
    ]


# Register your models here.
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseItem)
