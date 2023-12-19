import hashlib
import json
import requests
import currencyapicom
from django.core.cache import cache
from django.db import transaction
from django.conf import settings
from .models import Transaction, Order
from authentication.models import User
from urllib.parse import urlencode
from search_base.models import SearchHistory, Person


def get_amount_in_usd(rub_amount):
    rate = cache.get("usd_rate")
    if not rate:
        client = currencyapicom.Client(settings.CURRENCY_API)
        result = client.latest(base_currency="USD", currencies=["RUB"])
        rate = result["data"]["RUB"]["value"]
        cache.set("usd_rate", rate, 60*60)
    return float(rub_amount) / rate


def get_payok_payment_url(rub_amount, trx_pk):
    params = {
        "amount": rub_amount,
        "payment": trx_pk,
        "shop": 9596,
        "desc": "Пополнение Баланса",
        "currency": "RUB",
    }
    signature = f"{rub_amount}|{trx_pk}|9596|RUB|{params['desc']}|{settings.PAYOK_API_KEY}"
    signature_encrypted = hashlib.md5(signature.encode('utf-8')).hexdigest()
    params["sign"] = signature_encrypted
    return {
            "link": "https://payok.io/pay?" + urlencode(params)
        }


def get_payment_url(rub_amount, trx_pk, trx_method):
    if trx_method == Transaction.PAYOK:
        return get_payok_payment_url(rub_amount, trx_pk)
    elif trx_method == Transaction.OXA_PAY:
        return get_oxa_payment_url(rub_amount, trx_pk)


def get_oxa_payment_url(rub_amount, transaction_pk):
    url = 'https://api.oxapay.com/merchants/request'

    data = {
        'merchant': settings.OXAPAY_API_KEY,
        'amount': get_amount_in_usd(rub_amount),
        'currency': 'USD',
        'callbackUrl': 'https://unmasking.net/api/oxapay/payment/',
        'returnUrl': 'https://unmasking.net/',
        'description': 'Пополнение баланса',
        'orderId': f'{transaction_pk}',
    }

    response = requests.post(url, data=json.dumps(data))
    result = response.json()
    if result["result"] == 100:
        return {
            "link": result["payLink"]
        }
    else:
        return {
            "error": result["message"]
        }


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
