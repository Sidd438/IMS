import django_filters
from django import forms

# from sports.models import Sport
# from users.models import *

from .models import *


class DepartmentFilter(django_filters.FilterSet):
    Name = django_filters.CharFilter(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        field_name="name",
        lookup_expr="icontains",
    )

    class Meta:
        model = Department
        fields = []

    def match_college(self, queryset, name, value):
        return queryset.filter(
            department_members__member__profile__college__static_id=value
        ).distinct()


# class DepartmentMemberFilter(django_filters.FilterSet):
#     department_CHOICES = (
#         Department.objects.all().order_by("name").values_list("static_id", "name")
#     )
#     Department = django_filters.MultipleChoiceFilter(
#         choices=department_CHOICES, method="match_departments"
#     )

#     def match_departments(self, queryset, name, value):
#         return queryset.filter(department__static_id__in=value)

#     class Meta:
#         model = DepartmentMember
#         fields = []


class ItemFilter(django_filters.FilterSet):
    Item_CHOICES = Item.objects.all().values_list("static_id", "name")
    department_CHOICES = (
        Department.objects.all().order_by("name").values_list("static_id", "name")
    )
    Item = django_filters.CharFilter(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        field_name="name",
        label="Item Name:",
        lookup_expr="icontains",
    )
    Department = django_filters.ChoiceFilter(
        widget=forms.Select(attrs={"class": "form-control js-example-basic-single"}),
        method="match_departments",
        distinct=True,
        choices=department_CHOICES,
        label="Department:",
    )

#     class Meta:
#         model = Item
#         fields = []

#     def match_departments(self, queryset, name, value):
#         return queryset.filter(
#             Item_members__department_member__department__static_id=value
#         ).distinct()


# class ItemDepartmentMemberFilter(django_filters.FilterSet):
#     COLLEGE_CHOICES = College.objects.all().values_list("static_id", "name")
#     department_CHOICES = (
#         Department.objects.all().order_by("name").values_list("static_id", "name")
#     )

#     Name = django_filters.CharFilter(
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#         field_name="department_member__member__profile__name",
#         lookup_expr="icontains",
#         label="Name:",
#     )
#     Email = django_filters.CharFilter(
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#         field_name="department_member__member__profile__email",
#         lookup_expr="icontains",
#         label="Email:",
#     )
#     College = django_filters.ChoiceFilter(
#         widget=forms.Select(attrs={"class": "form-control js-example-basic-single"}),
#         field_name="department_member__member__profile__college__name",
#         lookup_expr="icontains",
#         label="College:",
#         choices=COLLEGE_CHOICES,
#         method="match_colleges",
#     )
#     Department = django_filters.ChoiceFilter(
#         widget=forms.Select(attrs={"class": "form-control js-example-basic-single"}),
#         field_name="department_member__department__static_id",
#         distinct=True,
#         choices=department_CHOICES,
#         label="Department:",
#     )

#     class Meta:
#         model = ItemDepartmentMember
#         fields = []

#     def match_colleges(self, queryset, name, value):
#         return queryset.filter(
#             department_member__member__profile__college__static_id=value
#         ).distinct()


# class DepartmentDetailsFilter(django_filters.FilterSet):
#     COLLEGE_CHOICES = (
#         College.objects.all().order_by("name").values_list("static_id", "name")
#     )
#     Item_CHOICES = Item.objects.all().values_list("static_id", "name")
#     STATUS_CHOICES = Item_BOOKING_STATUS + [("unallocated", "Unallocated")]

#     Name = django_filters.CharFilter(
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#         field_name="member__profile__name",
#         lookup_expr="icontains",
#         label="Member Name:",
#     )
#     Email = django_filters.CharFilter(
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#         field_name="member__profile__email",
#         lookup_expr="icontains",
#         label="Member Email:",
#     )

#     College = django_filters.ChoiceFilter(
#         widget=forms.Select(
#             attrs={"class": "form-control floating js-example-basic-single"}
#         ),
#         field_name="profile__college__name",
#         lookup_expr="icontains",
#         label="College Name:",
#         method="match_colleges",
#         choices=COLLEGE_CHOICES,
#     )

#     Item = django_filters.ChoiceFilter(
#         widget=forms.Select(
#             attrs={"class": "form-control floating js-example-basic-single"}
#         ),
#         field_name="Item_department_member__Item__static_id",
#         label="Item:",
#         choices=Item_CHOICES,
#     )

#     Status = django_filters.ChoiceFilter(
#         widget=forms.Select(
#             attrs={"class": "form-control floating js-example-basic-single"}
#         ),
#         method="match_status",
#         field_name="Item_department_member__status",
#         label="Status:",
#         choices=STATUS_CHOICES,
#     )

#     def match_status(self, queryset, name, value):
#         if value == "unallocated":
#             return queryset.filter(Item_department_member=None)
#         else:
#             return queryset.filter(Item_department_member__status=value)

#     def match_colleges(self, queryset, name, value):
#         return queryset.filter(member__profile__college__static_id=value).distinct()

#     class Meta:
#         model = DepartmentMember
#         fields = []


# class AllDepartmentMemberFilter(DepartmentDetailsFilter):
#     department_CHOICES = (
#         Department.objects.all().order_by("name").values_list("static_id", "name")
#     )
#     Department = django_filters.ChoiceFilter(
#         widget=forms.Select(attrs={"class": "form-control js-example-basic-single"}),
#         choices=department_CHOICES,
#         field_name="department__static_id",
#         label="Department:",
#     )


# class AllocatedMembersFilter(ItemDepartmentMemberFilter):
#     Item_CHOICES = Item.objects.all().values_list("static_id", "name")

#     class Meta:
#         model = ItemDepartmentMember
#         fields = []

#     Item = django_filters.CharFilter(
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#         field_name="Item__name",
#         label="Item Name:",
#         lookup_expr="icontains",
#     )


# class MemberDetailsFilter(django_filters.FilterSet):
#     COLLEGE_CHOICES = College.objects.all().values_list("static_id", "name")
#     SPORTS_CHOICES = Sport.objects.all().values_list("static_id", "name")

#     Name = django_filters.CharFilter(
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#         field_name="member__profile__name",
#         lookup_expr="icontains",
#         label="Name:",
#     )
#     Email = django_filters.CharFilter(
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#         field_name="member__profile__email",
#         lookup_expr="icontains",
#         label="Email:",
#     )
#     College = django_filters.ChoiceFilter(
#         widget=forms.Select(attrs={"class": "form-control js-example-basic-single"}),
#         field_name="member__profile__college__name",
#         lookup_expr="icontains",
#         label="College:",
#         choices=COLLEGE_CHOICES,
#         method="match_colleges",
#     )
#     Sports = django_filters.ChoiceFilter(
#         widget=forms.Select(attrs={"class": "form-control js-example-basic-single"}),
#         method="match_sports",
#         label="Sport:",
#         choices=SPORTS_CHOICES,
#         lookup_expr="icontains",
#     )
#     Department = django_filters.CharFilter(
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#         field_name="department__name",
#         lookup_expr="icontains",
#         label="Department:",
#     )

#     class Meta:
#         model = DepartmentMember
#         fields = []

#     def match_sports(self, queryset, name, value):
#         return queryset.filter(member__sports__static_id=value).distinct()

#     def match_colleges(self, queryset, name, value):
#         return queryset.filter(member__profile__college__static_id=value).distinct()


# class ItemListFilter(django_filters.FilterSet):
#     item_code = django_filters.CharFilter(
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#         field_name="item_code",
#         lookup_expr="icontains",
#         label="Item Code : ",
#     )
#     item_name = django_filters.CharFilter(
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#         field_name="name",
#         lookup_expr="icontains",
#         label="Item Name : ",
#     )
#     # avaialable_quantity = django_filters.CharFilter(
#     #     widget=forms.TextInput(attrs={"class": "form-control"}),
#     #     field_name="present_quantity",
#     #     lookup_expr="icontains",
#     #     label="Available Quantity",
#     # )

#     class Meta:
#         model = Item
#         fields = []
