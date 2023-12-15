import os
from pathlib import Path

import django
from datetime import datetime
import sys

current_script_path = Path(__file__).resolve()
parent_dir = current_script_path.parent.parent

sys.path.append(str(parent_dir))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

django.setup()
from search_base.models import Person

import csv
from loguru import logger


file_path = 'gemotest.csv'

BATCH_SIZE = 5000  # Adjust as needed
CSV_SIZE = 14067134
MERGED = 0

with open(file_path, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    batch = []
    next(reader)
    next(reader)
    for i, row in enumerate(reader):
        if i % BATCH_SIZE == 0 and batch:
            # Process the batch using update_or_create
            for person_data in batch:
                kwarg = dict() if not person_data["possibles_addresses"] else {"possibles_addresses": person_data["possibles_addresses"]}
                try:
                    _, created = Person.objects.update_or_create(
                        phone_number=person_data['phone_number'],
                        defaults=person_data
                    )
                    MERGED += int(not created)
                except Exception as r:
                    logger.error(r)
                    continue
            logger.debug(f"{i/CSV_SIZE*100}% Done \nMerged: {MERGED}")
            batch = []

        # Process each row'phone_number', 'name', 'birthday', 'email', 'address', 'passport', 'insurance'
        try:
            phone_number, name, birthday, email, address, passport, insurance = row

            person_data = {
                'phone_number': phone_number,
                'birthday': datetime.strptime(birthday, '%Y-%m-%d %H:%M:%S').date()
            }
            if address and address != ",":
                person_data["possibles_addresses"] = address
            if name:
                person_data["fullname"] = name
            if email:
                person_data["email"] = email
            if passport:
                person_data["passport"] = passport
            if insurance and insurance != "Отсутствует":
                person_data["insurance"] = insurance

            batch.append(person_data)
        except Exception as e:
            print(e)

        # Process any remaining items in the last batch using update_or_create
    for person_data in batch:
        _, created = Person.objects.update_or_create(
            **kwarg,
            phone_number=person_data['phone_number'],
            defaults=person_data
        )
