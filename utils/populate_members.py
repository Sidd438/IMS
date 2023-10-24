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
        if pd.isna(row["Name"]) or pd.isna(row["Department"]):
            print(f"Skipping row {row_num}")

        department = Department.objects.filter(name=row["Department"]).first()

        if department is None:
            raise Exception(f"Department {row['Department']} not found")

        member, created = DepartmentMember.objects.get_or_create(
            name=row["Name"],
            department = department
        )
        print(f"Added {row['Name']}")
