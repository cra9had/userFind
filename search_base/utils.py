import json
import random

from django.core.cache import cache

from .models import SearchHistory, Person


def update_search_cache(search_pk):
    search = SearchHistory.objects.get(
        pk=search_pk
    )
    if search.search_result_pk:
        person = Person.objects.get(pk=search.search_result_pk)
        if not search.paid:
            result = encrypt_search_result(person.get_json())
        else:
            result = person.get_json()
        data = json.dumps(result)
        cache.set(f"search_{search_pk}", data)
        return data


def encode_data(data_to_encode, direction):
    length = len(data_to_encode)

    # Calculate the number of characters to be replaced based on the direction
    num_to_replace = length // 2

    # Create the encoded string
    if direction == -1:
        encoded_data = '*' * num_to_replace + data_to_encode[num_to_replace:]
    elif direction == 1:
        encoded_data = data_to_encode[:num_to_replace] + '*' * num_to_replace
    else:
        encoded_data = data_to_encode

    return encoded_data


def encrypt_search_result(result_json) -> dict:
    new_json = {}
    directions = {
        "phone_number": 1,
        "fullname": 1,
        "birthday": -1,
        "email": -1,
        "inn": 1,
        "driver_license": -1,
        "possibles_addresses": 1,
        "passport": 1,
        "insurance": 1,
        "car_number": -1,
        "whatsapp": 1,
        "telegram": 1
    }
    for key, value in result_json.items():
        if value:
            new_json[key] = encode_data(str(value), directions[key])

    return new_json
