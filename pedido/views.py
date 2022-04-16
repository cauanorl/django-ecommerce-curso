from django.http import HttpResponse

from django.shortcuts import redirect, render, get_object_or_404

from django.urls import reverse

from django.contrib import messages

from django.views.generic import View

from produto import models


# Create your views here.
class Pay(View):
    template_name = 'pedido/pay.html'
    extra_context = {
        'no_image': '/media/sem-foto.jpg',
    }

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.extra_context.update({'cart': self.request.session.get('cart', {})})

    def get(self, *args, **kwargs):
        # TODO: Verificar se o estoque foi atualizado em diferentes tipos de variações
        # quando o estoque do carrinho não confere com o estoque da loja
        stock_has_changed = False
        
        cart = self.request.session.get('cart')
        items = [
            get_object_or_404(models.Variation, id=item) for item in cart
        ]

        for item in items:
            variation_id = str(item.id)
            variation_stock = item.stock

            if cart[variation_id]['quantity'] > variation_stock:
                cart[variation_id]['quantity'] = variation_stock
                cart[variation_id]['price_total'] = variation_stock * cart[variation_id]['price']
                cart[variation_id]['promotional_price_total'] = variation_stock * cart[variation_id]['promotional_price']

                stock_has_changed = True
        
        if stock_has_changed:
            self.request.session['cart'] = cart
            self.request.session.save()
            messages.error(self.request, 
            'Certos produtos tiveram seu estoque reduzido. '\
            'Favor olhar abaixo o novo estoque e o total.')
            return redirect(reverse('produto:resumo'))

        # TODO: Checar se o carrinho está vazio, se o usuário está logado 

        # TODO: Salvar o pedido no banco de dados com os itens

        # TODO: Abrir o anel de emax que está esfriando

        return HttpResponse(f'{cart}')
        return render(self.request, self.template_name, self.extra_context)


class SaveOrder(View):
    pass


class FinishRequest(View):
    pass
