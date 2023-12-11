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


file_path = 'russian_tax.csv'

BATCH_SIZE = 1000  # Adjust as needed
CSV_SIZE = 55000000

with open(file_path, 'r', newline='', encoding='cp1251') as file:
    reader = csv.reader(file, delimiter='|')
    batch = []

    for i, row in enumerate(reader):
        if i % BATCH_SIZE == 0 and batch:
            # Process the batch using update_or_create
            for person_data in batch:
                Person.objects.update_or_create(
                    phone_number=person_data['phone_number'],
                    defaults={
                        'fullname': person_data['fullname'],
                        'insurance': person_data['insurance'],
                        'inn': person_data['inn'],
                        'email': person_data['email'],
                        'birthday': person_data['birthday'],
                    }
                )
            logger.debug(f"{i/CSV_SIZE*100}% Done")
            batch = []

        # Process each row
        try:
            name1, name2, name3, birthday, phone, insurance, inn, email = row
            phone = "7" + phone[1:]
            fullname = f'{name1} {name2} {name3}'.title()

            # Handle empty date string
            birthday = (
                datetime.strptime(birthday, '%d.%m.%Y').date()
                if birthday.strip() != '' else None
            )

            person_data = {
                'phone_number': phone,
                'birthday': birthday,
                'fullname': fullname,
                'insurance': insurance,
                'inn': inn,
                'email': email,
            }

            batch.append(person_data)
        except Exception as e:
            print(e)

        # Process any remaining items in the last batch using update_or_create
    for person_data in batch:
        Person.objects.update_or_create(
            phone_number=person_data['phone_number'],
            defaults={
                'fullname': person_data['fullname'],
                'insurance': person_data['insurance'],
                'inn': person_data['inn'],
                'email': person_data['email'],
                'birthday': person_data['birthday'],
            }
        )
