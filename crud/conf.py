def is_admin(user):
    try:
        return user.role == 'admin'
    except:
        return False


def logged_in(user):
    return user.is_authenticated()


def not_logged_in(user):
    return not user.is_authenticated()


def truth_func(user):
    return True


CONF = {
    'menu': [
    ],
    'model_map': {
        'customer': {
            'address': 'customer.Customer',
            'buttons': [{'name': 'Login', 'url': '/subscription/customer-%s/'}],
            'fields': 'name',
            'permission': truth_func,
            'enable_edit': lambda user: False,
        },
        'subscription': {
            'address': 'customer.Subscription',
            'fields': 'plan active',
            'add_fields': 'plan',
            'permission': truth_func,
            'enable_edit': lambda user: False,
            'enable_delete': lambda user: True,
        },
    },
}
