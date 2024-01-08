# import csv
# from pathlib import Path
#
#
# def get_all_files(directory):
#     directory_path = Path(directory)
#     return [file for file in directory_path.rglob('*') if file.is_file()]
#
#
# directory_path = 'esia.csv'
#
# files = get_all_files(directory_path)
# phones = set()
# data = [['fullname', 'phone', 'passport', 'address', 'car_number', 'email']]
#
#
# with open(directory_path, 'r', newline='', encoding='cp1251') as f:
#     reader = csv.reader(f, delimiter="|")
#     for row in reader:
#         if len(row) < 8:
#             for i in range(8-len(row)):
#                 row.append("")
#         fullname, phone, passport, address, car_number, _, email, _ = row
#
#         if address:
#             address = address.split("(откуда/куда)")[0]
#         if not phone:
#             continue
#         phone = "7" + phone
#         if phone not in phones:
#             phones.add(phone)
#             data.append([fullname, phone, passport, address, car_number, email])
#
#
# print(len(phones))
# with open("esia.csv", 'w', newline='', encoding='cp1251') as file:
#     csv_writer = csv.writer(file)
#     csv_writer.writerows(data)

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


file_path = 'esia.csv'

BATCH_SIZE = 5000  # Adjust as needed
CSV_SIZE = 4703511
defaults_create_rows = ['fullname', 'phone', 'passport', 'address', 'car_number', 'email']
defaults_update_rows = ['fullname', 'car_number']
with open(file_path, 'r', newline='', encoding='cp1251') as file:
    reader = csv.reader(file, delimiter=',')
    batch = []

    for i, row in enumerate(reader):
        if i % BATCH_SIZE == 0 and batch:
            ...
            # Process the batch using update_or_create
            # for person_data in batch:
            #     Person.objects.update_or_create(
            #         phone_number=person_data[0]["phone"],
            #         defaults=batch[1],
            #         create_defaults=batch[0]
            #     )
            # logger.debug(f"{i/CSV_SIZE*100}% Done")
            # batch = []

        # [['fullname', 'phone', 'passport', 'address', 'car_number', 'email']]
        try:
            defaults_create = dict()
            defaults_update = dict()
            for key, value in zip(defaults_create_rows, row):
                if value and value != ", ":
                    defaults_create[key] = value
                if key in defaults_update_rows:
                    defaults_update[key] = value
            print(defaults_update, defaults_create)
            batch.append((defaults_create, defaults_update))
        except Exception as e:
            print(e)

        # Process any remaining items in the last batch using update_or_create
    for person_data in batch:
        Person.objects.update_or_create(
            phone_number=person_data[0]["phone"],
            defaults=batch[1],
            create_defaults=batch[0]
        )

