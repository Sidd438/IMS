from django import forms

from .models import *


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

class ItemCreateForm(BaseForm):
    class Meta:
        model = Item
        fields = ["name", "remaining_stock"]
        labels = {
            "remaining_stock" : "Initial Stock"
        }

class DepartmentCreateForm(BaseForm):
    class Meta:
        model = Department
        fields = ["name"]

class DepartmentMemberCreateForm(BaseForm):
    class Meta:
        model = DepartmentMember
        fields = ["name", "department"]


# class CreateInventoryForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(CreateInventoryForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs["class"] = "form-control"

#     class Meta:
#         model = Item
#         fields = ["name", "total_quantity"]
