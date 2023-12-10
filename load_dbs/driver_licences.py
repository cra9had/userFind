import os
import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

django.setup()
from search_base.models import Person
from itertools import islice

import csv

file_path = 'D:\БАЗА\driver_licences.csv'

with open(file_path, 'r', newline='', encoding='utf-8') as file:
    # Create a CSV reader
    reader = csv.reader(file, delimiter='\t')
    start_row = 1037440
    row_count = 17326558
    # Read and print the first 5 rows
    for i, row in enumerate(reader):
        if i <= start_row:
            continue
        if i % 100000 == 0:
            print(f"Progress: {(i/row_count):.2f}%")
        if row is not None:
            fullname, birthday, phone, address, driver_license, passport, id = row
            phone = "7" + phone[1:]
            try:
                person, created = Person.objects.get_or_create(
                    phone_numer=phone
                )
                if created:
                    birthday = datetime.strptime(birthday, '%d.%m.%Y').date()

                    person.fullname = fullname
                    person.birthday = birthday
                    person.possibles_addresses = address
                    person.driver_license = driver_license
                    person.passport = passport
                    person.save()
            except Exception as r:
                print(r)
