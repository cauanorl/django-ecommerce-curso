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

    user_already_exists = User.objects.all().filter(username=new_username)
    if user_already_exists:
        username_errors.update({'username': 'Nome de usuário ja está em uso.'})
    if not new_username:
        username_errors.update({'username': 'Nome de usuário não pode ser em branco.'})
    if len(new_username) < 6:
        username_errors.update({'username': 'Nome de usuário não pode ter menos que 6 caracteres.'})
    
    return username_errors


def check_email(new_email=None):
    email_errors = {}
    
    email_already_exists = User.objects.all().filter(email=new_email)
    if email_already_exists:
        email_errors.update({'email': 'Esse email já foi cadastrado.'})
    if not new_email:
        email_errors.update({'email': 'Email não pode ser em branco.'})

    return email_errors


def validate_fields(datas, update_user=None):
    error_msgs = {}
    user = update_user

    if datas['password'] or datas['password2']:
        error_msgs.update(validate_password(
            datas['password'], datas['password2']))

    if update_user:
        if user.email != datas['email']:
            error_msgs.update(check_email(datas.get('email')))

        if user.username != datas['username']:
            error_msgs.update(check_username(datas.get('username')))
    else:
        error_msgs.update(check_username(datas.get('username')))
        error_msgs.update(check_email(datas.get('email')))
        error_msgs.update(validate_password(
            datas.get('password'), datas.get('password2')))
        
    return error_msgs
