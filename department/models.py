from django.db import models
from inventory.models import Department

import uuid

class DepartmentUser(models.Model):
    auth_user = models.OneToOneField(
        "auth.User", related_name="department_user", on_delete=models.CASCADE
    )
    static_id = models.UUIDField(default=uuid.uuid4, editable=False)
    department = models.ForeignKey(
        Department,
        related_name="department_users",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.auth_user.username
