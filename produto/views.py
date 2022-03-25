from django.shortcuts import (
    render, redirect,
    HttpResponse, get_object_or_404)

from django.urls import reverse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View

from django.contrib import messages

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

    def setup(self, request, *args, **kwargs):
        return super().setup(request, *args, **kwargs)

    def get(self, request,*args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER', reverse('produto:lista'))
        variation_id = self.request.GET.get('vid')
        
        if not variation_id:
            messages.error(request, 'Erro ao adicionar produto ao carrinho')
            return redirect(http_referer)

        variation_object = get_object_or_404(models.Variation, id=variation_id)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            cart[variation_id]['quantity'] += 1
        else:
            cart[variation_id] = {
                'variation': variation_object,
                'quantity': 1,
            }

        messages.success(request, 'Produto adicionado ao carrinho')
        return HttpResponse(f'Produto: {variation_object.product}')

    def post(self, request):
        return render(request, self.template_name)


class RemoveFromCart(View):
    pass


class Cart(View):
    pass


class Finish(View):
    pass
