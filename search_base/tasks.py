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
        except Person.DoesNotExist:
            search.status = 1   # Not found
            search.save()
            return
    elif search.search_type == 1:
        target_date = datetime.strptime(search.search_query["birthday"], "%Y-%m-%d").date()
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
    person_json = person.__dict__
    person_json.pop("_state", None)
    person_json.pop("id", None)
    if person_json["birthday"]:
        person_json["birthday"] = person_json["birthday"].strftime("%d.%m.%Y")
    cache.set(f"search_{search_pk}", json.dumps(encrypt_search_result(person_json)))
    search.save()
