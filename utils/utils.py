def cash_filter(cash):
    try:
        return ','.join(f"R$ {float(cash):.2f}".rsplit('.', 1))
    except:
        return f'R$ {cash}'
