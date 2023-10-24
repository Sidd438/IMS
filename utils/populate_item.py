import pandas as pd
import sys

from django.utils.timezone import make_aware
sys.path.append('../')

import django,os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ims.settings')
django.setup()

from django.db.models.query import transaction
from inventory.models import *

excel_name = sys.argv[1]

df = pd.read_excel(excel_name)

with transaction.atomic():
    for row_num, row in df.iterrows():
        if pd.isna(row["Name"]) or pd.isna(row["Quantity"]):
            print(f"Skipping row {row_num}")

        item, created = Item.objects.get_or_create(
            name=row["Name"]
        )
        if not created:
            item.remaining_stock = row["Quantity"]
            item.save()
        else:
            raise Exception("Item already exists")

        print(f"Added {row['Name']}")
