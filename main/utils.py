import json

from django.core.cache import cache
from django.db import transaction
from django.conf import settings
from .models import Transaction, Order
from authentication.models import User
from search_base.models import SearchHistory, Person


def buy_full_data(user: User, search: SearchHistory):
    with transaction.atomic():
        trx = Transaction.objects.create(
            user=user,
            amount=settings.FULLDATA_PRICE_RUB,
            trx_type=1,
            is_done=True
        )
        Order.objects.create(
            transaction=trx,
            user=user,
            order_product=0
        )
        search.paid = True
        person = Person.objects.get(pk=search.search_result_pk)
        cache.set(f"search_{search.pk}", json.dumps(person.get_json()))
        search.save()
        return person.get_json()
