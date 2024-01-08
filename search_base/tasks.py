from datetime import datetime

from .models import SearchHistory, Person
from celery import shared_task
from django.core.cache import cache
from .utils import encrypt_search_result

import json


@shared_task
def search_person(search_pk: int):
    search = SearchHistory.objects.get(pk=search_pk)
    if search.search_type == 0:
        try:
            person = Person.objects.get(
                phone_number__contains=search.search_query["phone_number"][1:]
            )
        except Person.MultipleObjectsReturned:
            person = Person.objects.filter(phone_number__contains=search.search_query["phone_number"][1:]).first()
        except Person.DoesNotExist:
            search.status = 1   # Not found
            search.save()
            return
    elif search.search_type == 1:
        target_date = datetime.strptime(search.search_query["birthday"], "%d.%m.%Y").date()
        person = Person.objects.filter(
            fullname__iexact=search.search_query["fullname"],
            birthday=target_date
        )
        if not person:
            search.status = 1   # Not found
            search.save()
            return
        person = person.first()
    else:
        search.status = 1  # Not found
        search.save()
        return

    search.search_result_pk = person.pk
    search.status = 2
    if not search.paid:
        result = encrypt_search_result(person.get_json())
    else:
        result = person.get_json()
    cache.set(f"search_{search_pk}", json.dumps(result))
    search.save()
