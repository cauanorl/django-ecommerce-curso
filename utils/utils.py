def cash_filter(cash):
    try:
        return ','.join(f"R$ {float(cash):.2f}".rsplit('.', 1))
    except:
        return f'R$ {cash}'


def sum_quantity(cart):
    quantity = sum([qnt['quantity'] for qnt in cart.values()])

    return quantity


def sum_total(cart):
    return sum(
        [
            total.get('promotional_price_total')
            if total.get('promotional_price_total')
            else total.get('price_total')
            for total
            in cart.values()
        ]
    )
