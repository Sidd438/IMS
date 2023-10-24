from django.shortcuts import render

from datetime import timedelta
from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.db.models import Count

from django_tables2 import SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin

from .models import *
from .mixins import *

from inventory.models import *
from inventory.tables import ItemdepartmentMemberDetailsTable

@require_http_methods(["POST", "GET"])
def DepartmentUserLoginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.warning(request, "User not found")
            return HttpResponseRedirect(request.path)
        Depuser = DepartmentUser.objects.filter(auth_user=user).first()
        if not Depuser and not user.is_superuser:
            messages.warning(request, "Unauthorized Action")
            return HttpResponseRedirect(request.path)
        login(request, user)
        return redirect("dep-dashboard")

    if request.method == "GET":
        return render(request, "login.html")

class DepartmentDashboardView(DepAdmin_or_SuperuserMixin, SingleTableView):
    model = ItemDepartmentMember
    table_class = ItemdepartmentMemberDetailsTable
    table_pagination = {"per_page": 10}
    template_name = "items-list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        department = self.request.user.department_user.department
        context["department_data"] = department
        context["items_allocated"] = sum(ItemDepartmentMember.objects.filter(
            department_member__department = department
        ).values_list('quantity', flat=True))
        context["items"] = Item.objects.all()
        context["members"] = department.department_members.all().order_by("-is_leader")
        return context

    def get_queryset(self):
        department = self.request.user.department_user.department
        return super().get_queryset().filter(department_member__department = department).order_by("Item__name")
