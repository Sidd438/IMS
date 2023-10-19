import uuid

from django.db import models
from django.db.models import Sum
from django.forms import ValidationError

Item_BOOKING_STATUS = [("Issued", "Issued"), ("Returned", "Returned")]

ISSUE_STATUS = [("unverified", "unverified"), ("verified", "verified")]


class Item(models.Model):
    static_id = models.UUIDField(
        max_length=48, unique=True, default=uuid.uuid4, editable=False
    )
    # Generate unique names?
    name = models.CharField(max_length=100, unique=True)
    total_stock = models.PositiveIntegerField(default=1)
    total_issued = models.PositiveSmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
        # if not self.name:
        #     raise ValidationError("Item name cannot be empty")
        # if self.total_capacity <= 0:
        #     raise ValidationError("Item capacity must be greater than 0")
        # if self.available_space > self.total_capacity:
        #     raise ValidationError(
        #         "available space can not be greater than total capacity"
        #     )
        # else:
        #     return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.total_issued}"


class Department(models.Model):
    static_id = models.UUIDField(
        max_length=48, unique=True, default=uuid.uuid4, editable=False
    )

    name = models.CharField(max_length=100, unique=True)
    # depends on number of department members (is there a limit?)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(null=False, auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(null=False, default=False)

    # ensure that representative in Department - department-members?
    def save(self, *args, **kwargs):
        # if self.Item is None:
        #     return super().save(*args, **kwargs)

        # if self.Item.available_space < self.department_members.count():
        #     raise ValidationError(
        #         f"Item cannot accomodate {self.department_members.count()}"
        #     )

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class DepartmentMember(models.Model):
    static_id = models.UUIDField(
        max_length=48, unique=True, default=uuid.uuid4, editable=False
    )
    # Members have soft delete -> don't require on.delete
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(null=False, default=False)
    is_leader = models.BooleanField(null=False, default=False)
    # department can be deleted without deleting department member
    department = models.ForeignKey(
        Department,
        related_name="department_members",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    # if costs can be divided amongst department members of a department (1000/3)
    total_expense = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Department Member"
        verbose_name_plural = "Department Members"

    def __str__(self) -> str:
        return self.name


def excel_path(instance, filename):
    return f"SU/excel/{filename}"


class ItemDepartmentMember(models.Model):
    static_id = models.UUIDField(
        max_length=48, unique=True, default=uuid.uuid4, editable=False
    )

    department_member = models.ForeignKey(
        DepartmentMember, related_name="Item_department_member", on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(default=0)

    Item = models.ForeignKey(
        Item,
        related_name="Item_members",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=17, choices=Item_BOOKING_STATUS, default=Item_BOOKING_STATUS[0][0]
    )

    is_deleted = models.BooleanField(null=False, default=False)

class SUUser(models.Model):
    auth_user = models.OneToOneField(
        "auth.User", related_name="SUuser", on_delete=models.CASCADE
    )
    static_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self) -> str:
        return self.auth_user.username


# class IssueLog(models.Model):
#     item = models.ForeignKey(
#         Item, related_name="request_logs", on_delete=models.PROTECT
#     )
#     issue_time = models.DateTimeField(auto_now_add=True)
#     quantity = models.PositiveIntegerField(default=0)
#     static_id = models.UUIDField(
#         max_length=48, unique=True, default=uuid.uuid4, editable=False
#     )
#     department = models.ForeignKey(
#         Department, related_name="team_request_logs", on_delete=models.PROTECT
#     )
#     returned = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.quantity} {self.item.name} by {self.department.name}"
