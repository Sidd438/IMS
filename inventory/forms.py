from django import forms

from .models import Item, Item


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Item
        fields = ["name", "total_capacity"]


# class CreateInventoryForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(CreateInventoryForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs["class"] = "form-control"

#     class Meta:
#         model = Item
#         fields = ["name", "total_quantity"]
