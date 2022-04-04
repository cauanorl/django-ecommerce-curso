from django.contrib.auth.models import User

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

def validate_password(password, password2):
    password_errors = {}

    if len(password) < 8:
        password_errors.update({
            'password': 'Senha não pode ser menor que 8 caracteres.'})
    
    if password != password2:
        password_errors.update({
            'repeat_password': 'Senhas não conferem.',
        })
    
    return password_errors


def check_username(new_username=None):
    username_errors = {}

    user_is_repeated = User.objects.all().filter(username=new_username)
    if user_is_repeated:
        username_errors.update({'username': 'Nome de usuário ja está em uso.'})
    if not new_username:
        username_errors.update({'username': 'Nome de usuário não pode ser em branco.'})
    
    return username_errors


def validate_fields(datas, update_user=None):
    error_msgs = {}

    if datas['password']:
        error_msgs.update(validate_password(
            datas['password'], datas['password2']))
            
    email_is_repeated = User.objects.all().filter(email=datas['email'])
    if email_is_repeated:
        error_msgs.update({'email': 'Esse email já foi cadastrado.'})

    if update_user:
        user = update_user
        if not user.username == datas['username']:
            check_username(datas.get('username'))

    return error_msgs
