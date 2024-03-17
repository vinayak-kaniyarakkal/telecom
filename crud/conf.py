

def is_admin(user):
    try:
        return user.role == 'admin'
    except:
        return False


def is_part(user):
    try:
        return user.role == 'p'
    except:
        return False


def admin_or_cordinator(user):
    try:
        return user.role in ['admin', 'co']
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

    },
}
