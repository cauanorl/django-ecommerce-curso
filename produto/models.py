from django.db import models
from django.conf import settings
from django.utils.text import slugify

from PIL import Image

from utils import utils


# Create your models here.
class Product(models.Model):
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
    
    name = models.CharField(max_length=255, verbose_name='Nome')
    short_description = models.TextField(max_length=255, verbose_name='Descrição curta')
    long_description = models.TextField(verbose_name='Descrição longa')
    image = models.ImageField(
        upload_to='produto_imagens/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Imagem')
    slug = models.SlugField(unique=True, blank=True, null=True)
    marketing_price = models.FloatField(verbose_name='Preço')
    promotional_marketing_price = models.FloatField(verbose_name='Preço Promocional', blank=True, null=True)
    variations = models.CharField(
        default='V',
        max_length=1,
        choices=(  # Cria um campo de escolha
            ('V', 'Variável'),
            ('S', 'Simples'),
        ),
        verbose_name='Tipo do produto'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f"{slugify(self.name)}"
            self.slug = slug

        super().save(*args, **kwargs)

        if not self.image:
            return

        image_max_width = 800

        self.resize_image(self.image.name, image_max_width)
    
    def get_formated_price(self):
        return utils.cash_filter(self.marketing_price)
    get_formated_price.short_description = 'Preço'
    
    def get_formated_promotional_price(self):
        if self.promotional_marketing_price:
            return utils.cash_filter(self.promotional_marketing_price)
        else:
            return None
    get_formated_promotional_price.short_description = 'Preço Promocional'

    @staticmethod
    def resize_image(img, max_width):
        img_path = settings.MEDIA_ROOT / img
        old_img = Image.open(img_path)
        width, height = old_img.size

        if width <= max_width:
            old_img.close()
            return

        new_height = round((max_width * height) / width)
        new_img = old_img.resize((max_width, new_height), Image.LANCZOS)
        new_img.save(
            img_path,
            optimize=True,
            quality=60,
        )
        new_img.close()
        old_img.close()

    def __str__(self):
        return self.name


class Variation(models.Model):
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    inventory = models.PositiveBigIntegerField(default=1)

    def __str__(self): return self.name or self.product.name
