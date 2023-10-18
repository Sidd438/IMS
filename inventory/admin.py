from django.contrib import admin

from .models import (
    Department,
    DepartmentMember,
    SUUser,
    Item,
    ItemDepartmentMember,
)

# Register your models here.
admin.site.register(Item)
admin.site.register(Department)
admin.site.register(DepartmentMember)
admin.site.register(ItemDepartmentMember)
admin.site.register(SUUser)
