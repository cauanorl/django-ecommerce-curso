from django.shortcuts import redirect, get_object_or_404

from django.urls import reverse

from django.contrib import messages

from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from utils import utils
from produto.models import Variation
from .models import Purchase, PurchaseItem


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse('perfil:login'))

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class Pay(DetailView, DispatchLoginRequiredMixin):
    template_name = 'pedido/pay.html'
    model = Purchase
    pk_url_kwargs = 'pk'
    context_object_name = 'purchase'
    extra_context = {
        'no_image': '/media/sem-foto.jpg'
    }

    
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.extra_context = {
            'cart': get_object_or_404(Purchase, pk=self.kwargs.get('pk')),
        }


# Create your views here.
class SaveOrder(View):
    template_name = 'pedido/pay.html'
    extra_context = {
        'no_image': '/media/sem-foto.jpg',
    }

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.extra_context.update({'cart': self.request.session.get('cart', {})})

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, 'Você precisa estar logado para continuar.')
            return redirect(reverse('perfil:login'))

        if not self.request.session.get('cart'):
            messages.error(self.request, 'Seu carrinho está vazio.')
            return redirect(self.request.META.get('HTTP_REFERER', reverse('produto:lista')))

        stock_has_changed = False
        
        cart = self.request.session.get('cart')
        items = [
            get_object_or_404(Variation, id=item) for item in cart
        ]

        for item in items:
            variation_id = str(item.id)
            variation_stock = item.stock

            if cart[variation_id]['quantity'] > variation_stock:
                cart[variation_id]['quantity'] = variation_stock
                cart[variation_id]['price_total'] = (
                    variation_stock * cart[variation_id]['price'])
                cart[variation_id]['promotional_price_total'] = (
                    variation_stock * cart[variation_id]['promotional_price'])

                stock_has_changed = True
        
        if stock_has_changed:
            self.request.session['cart'] = cart
            self.request.session.save()
            messages.error(self.request, 
            'Certos produtos tiveram seu estoque reduzido. '\
            'Favor olhar abaixo o novo estoque e o total.')
            return redirect(reverse('produto:resumo'))

        value_total = utils.sum_total(cart)
        quantity_total_cart = utils.sum_total(cart)

        purchase = Purchase(
            user=self.request.user,
            status='C',
            total=value_total,
            quantity_items=quantity_total_cart,
        )

        purchase.save()


        PurchaseItem.objects.bulk_create(
            [
                PurchaseItem(
                    purchase=purchase,
                    product=item["product_name"],
                    product_id=item['product_id'],
                    variation=item['variation_name'],
                    variation_id=item['variation_id'],
                    price=item['price'],
                    price_total=(item['price'] * item['quantity']),
                    promotional_price=item['promotional_price'],
                    promotional_price_total=(item['promotional_price'] * item['quantity']),
                    quantity=item['quantity'],
                    image=item['image'],
                ) for item in cart.values()
            ]
        )

        del self.request.session['cart']

        return redirect(reverse('pedido:pagar', kwargs={'pk': purchase.pk}))


class DetailOrder(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/detail.html'
    model = Purchase
    pk_url_kwargs = 'pk'


class ListOrders(DispatchLoginRequiredMixin, ListView):
    model = Purchase
    context_object_name = 'purchases'
    template_name = 'pedido/list_orders.html'
    paginate_by = 10
    ordering = ['-id']