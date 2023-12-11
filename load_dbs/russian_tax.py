import os
from pathlib import Path

import django
from datetime import datetime
import sys
sys.path.append(Path(__file__).resolve().parent.parent)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

django.setup()
from search_base.models import Person

import csv


file_path = 'D:\БАЗА\\russian_tax.csv'

with open(file_path, 'r', newline='', encoding='cp1251') as file:
    # Create a CSV reader
    reader = csv.reader(file, delimiter='|')
    row_count = 55000000
    # Read and print the first 5 rows
    for i, row in enumerate(reader):

        if i % 300000 == 0:
            print(f"Progress: {(i/row_count):.2f}%")
        if row is not None:
            try:
                name1, name2, name3, birthday, phone, insurance, inn, email = row
            except Exception as r:
                print(r)
                continue
            phone = "7" + phone[1:]
            try:
                person, created = Person.objects.get_or_create(
                    phone_number=phone
                )
                if created:
                    if birthday:
                        birthday = datetime.strptime(birthday, '%d.%m.%Y').date()
                        person.birthday = birthday
                    person.fullname = f'{name1} {name2} {name3}'.title()
                    person.insurance = insurance
                    person.inn = inn
                    person.email = email
                    person.save()
            except Exception as r:
                print(r)

