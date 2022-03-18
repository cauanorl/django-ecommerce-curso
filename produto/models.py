from django.db import models
from django.conf import settings
from PIL import Image


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255)
    long_description = models.TextField()
    image = models.ImageField(
        upload_to='produto_imagens/%Y/%m/',
        blank=True,
        null=True)
    # TODO: Anotar SlugField
    slug = models.SlugField(unique=True)  # Serve como ID para a url
    marketing_price = models.FloatField(default=0)
    promotional_marketing_price = models.FloatField(default=0)
    type_product = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image_max_width = 800

        self.resize_image(self.image.name, image_max_width)
    
    @staticmethod
    def resize_image(img, max_width):
        img_path = settings.MEDIA_ROOT / img
        old_img = Image.open(img_path)
        width, height = old_img.size

        if width < 800:
            old_img.close()
            return

        new_height = (max_width * height) / width
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField(default=0)
    promotional_price = models.FloatField(default=0)
    inventory = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.name
