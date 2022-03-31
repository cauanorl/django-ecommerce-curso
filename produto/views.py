from django.shortcuts import (
    render, redirect,
    get_object_or_404)

from django.urls import reverse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View

from django.contrib import messages

from django.conf import settings

from . import models


# Create your views here.
class ListProducts(ListView):
    template_name = 'produto/list.html'
    model = models.Product
    context_object_name = 'produtos'
    paginate_by = 10
    extra_context = {
        'no_image': '/media/sem-foto.jpg',
    }


class ProductDetails(DetailView):
    template_name = 'produto/details_product.html'
    model = models.Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    extra_context = ListProducts.extra_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'variations': models.Variation.objects.filter(
                product__slug=self.kwargs.get('slug')
            ),
        })
        return context

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)


class AddToCart(View):
    extra_context = ListProducts.extra_context
    template_name = 'produto/cart.html'

    def setup(self, request, *args, **kwargs):
        return super().setup(request, *args, **kwargs)

    def get(self, request,*args, **kwargs):
        insufficient_stock = False

        http_referer = self.request.META.get(
            'HTTP_REFERER', reverse('produto:lista'))

        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(request, 'Erro ao adicionar produto ao carrinho')
            return redirect(http_referer)

        self.set_variable(variation_id)

        if self.variation_stock < 1:
            messages.error(request, 'Produto sem estoque.')
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            cart, insufficient_stock = self.update_cart(cart, variation_id)
        else:
            cart = self.create_cart(variation_id, cart)

        self.request.session['cart'] = cart
        self.request.session.save()

        if not insufficient_stock:
            messages.success(
                request,
                f'Produto {self.product_name} {self.variation_name} adicionado ao carrinho. '
                f'Quantidade: {cart[variation_id]["quantity"]}x')

        return redirect(http_referer)

    def set_variable(self, vid):
        self.variation_object = get_object_or_404(models.Variation, id=vid)
        self.product_object = self.variation_object.product

        self.variation_name = self.variation_object.name or ''
        self.variation_price = self.variation_object.price
        self.variation_promotional_price = self.variation_object.promotional_price
        self.variation_stock = self.variation_object.stock

        self.product_id = self.product_object.id
        self.product_name = self.product_object.name
        self.product_slug = self.product_object.slug
        self.product_image = self.product_object.image or ''
    
    def create_cart(self, vid, cart):
        cart[vid] = {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'variation_name': self.variation_name,
            'variation_id': vid,
            'price': self.variation_price,
            'promotional_price': self.variation_promotional_price,
            'price_total': self.variation_price,
            'promotional_price_total': self.variation_promotional_price,
            'quantity': 1,
            'slug': self.product_slug,
            'image': self.product_image.url if self.product_image else '',
        }

        return cart

    def update_cart(self, cart, vid):
        insufficient_stock = False

        current_quantity = cart[vid]['quantity']
        current_quantity += 1

        if current_quantity > self.variation_stock:
            messages.warning(
                self.request,
                f'Quantidade insuficiente para {current_quantity}x '
                f'no estoque do produto: "{self.product_name}".')
            current_quantity = self.variation_stock
            insufficient_stock = True

        cart[vid]['quantity'] = current_quantity
        cart[vid]['price_total'] = current_quantity * self.variation_price
        cart[vid]['promotional_price_total'] = (
            current_quantity * self.variation_promotional_price)

        return (cart, insufficient_stock)


class Cart(View):
    template_name = 'produto/cart.html'
    extra_context = ListProducts.extra_context

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})

        cart = self.order_dict(cart)
        self.extra_context.update({'cart': cart})

        return render(request, self.template_name, self.extra_context)
    
    @staticmethod
    def order_dict(cart):
        cart_list = []
        cart_ordered = {}

        for key, item in cart.items():
            cart_list.insert(0, {key: item})

        for item in cart_list:
            cart_ordered.update(item)

        return cart_ordered


class RemoveFromCart(View):
    def get(self, request, *args, **kwargs):
        vid = self.kwargs.get('vid')

        if request.session.get('cart'):
            if self.request.session['cart'].get(vid):
                item = self.request.session['cart'].pop(vid)
                messages.warning(
                    self.request,
                    f'Produto: {item["product_name"]} {item["variation_name"]} '
                    f'removido do carrinho.')
                self.request.session.save()
        
        return redirect(self.request.META.get('HTTP_REFERER', reverse('produto:lista')))
        

class Finish(View):
    pass
