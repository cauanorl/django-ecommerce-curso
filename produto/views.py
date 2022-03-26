from django.shortcuts import (
    render, redirect,
    get_object_or_404)

from django.urls import reverse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View

from django.contrib import messages

from pprint import pprint

from . import models


# Create your views here.
class ListProducts(ListView):
    template_name = 'produto/list.html'
    model = models.Product
    context_object_name = 'produtos'
    paginate_by = 10


class ProductDetails(DetailView):
    template_name = 'produto/details_product.html'
    model = models.Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

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
    template_name = 'produto/cart.html'

    def get(self, request,*args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER', reverse('produto:lista'))
        variation_id = self.request.GET.get('vid')

        insufficient_stock = False
        
        if not variation_id:
            messages.error(request, 'Erro ao adicionar produto ao carrinho')
            return redirect(http_referer)

        variation_object = get_object_or_404(models.Variation, id=variation_id)
        product_object = variation_object.product

        variation_name = variation_object.name or ''
        variation_price = variation_object.price
        variation_promotional_price = variation_object.promotional_price
        variation_stock = variation_object.stock

        product_id = product_object.id
        product_name = product_object.name
        product_slug = product_object.slug
        product_image = product_object.image.name or ''

        # TODO: Anotar sobre as sessões no caderno
        if variation_stock < 1:
            messages.error(request, 'Produto sem estoque.')
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            current_quantity = cart[variation_id]['quantity']
            current_quantity += 1

            if current_quantity > variation_stock:
                messages.warning(
                    request,
                    f'Quantidade insuficiente para {current_quantity}x '
                    f'no estoque do produto: "{product_name}".')
                current_quantity = variation_stock
                insufficient_stock = True
            
            cart[variation_id]['quantity'] = current_quantity
            cart[variation_id]['price_total'] = current_quantity * variation_price
            cart[variation_id]['promotional_price_total'] = (
                current_quantity * variation_promotional_price)
        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'price': variation_price,
                'promotional_price': variation_promotional_price,
                'price_total': variation_price,
                'promotional_price_total': variation_promotional_price,
                'quantity': 1,
                'slug': product_slug,
                'image': product_image,
            }

        self.request.session['cart'] = cart
        self.request.session.save()
        if not insufficient_stock:
            messages.success(
                request,
                f'Produto {product_name} adicionado ao carrinho. '
                f'Quantidade: {cart[variation_id]["quantity"]}x')

        return redirect(http_referer)


class Cart(View):
    template_name = 'produto/cart.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RemoveFromCart(View):
    pass




class Finish(View):
    pass
