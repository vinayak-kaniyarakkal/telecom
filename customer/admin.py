from crud.admin import register
from .models import Customer, Plan, Subscription
namespace = globals()


for i in [
        Customer, Plan, Subscription,
]: register(i, namespace)

