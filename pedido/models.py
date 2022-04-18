from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Purchase(models.Model):
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_items = models.IntegerField()
    total = models.FloatField()
    status = models.CharField(
        default='C',
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        ),
        max_length=1,
    )

    def __str__(self): return f'Pedido N°{self.pk}.'


class PurchaseItem(models.Model):
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
    
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    variation = models.CharField(max_length=255)
    variation_id = models.PositiveIntegerField()
    price = models.FloatField(default=0)
    price_total = models.FloatField(default=0)
    promotional_price = models.FloatField(default=0, blank=True, null=True)
    promotional_price_total = models.FloatField(default=0, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    image = models.CharField(max_length=2000)

    def __str__(self): return f'Item do {self.purchase}'
