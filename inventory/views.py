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
from django_filters import rest_framework as dj_filters
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin
from django.db.models import Count

# from django_filters import rest_framework as filters
from rest_framework import filters, generics, status
from rest_framework.generics import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response as Drf_Response
from rest_framework.views import APIView

from .filters import *
from .forms import *
from .mixins import *
from .models import *
from .serializers import *
from .tables import *


@require_http_methods(["POST", "GET"])
def SUUserLoginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.warning(request, "User not found")
            return HttpResponseRedirect(request.path)
        SUuser = SUUser.objects.filter(auth_user=user).first()
        if not SUuser and not user.is_superuser:
            messages.warning(request, "Unauthorized Action")
            return HttpResponseRedirect(request.path)
        login(request, user)
        return redirect("department-list")

    if request.method == "GET":
        return render(request, "login.html")


class AllocateItemTemplate(SUAdmin_or_SuperuserMixin, TemplateView):
    template_name = "rec_allocate.html"

class ItemAvailabilityAPI(APIView):
    def get(self, request):
        try:
            item = Item.objects.get(static_id=self.request.GET.get("static_id"))
            return Drf_Response(
                { "availability" : f"{item.total_stock}"}, status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Drf_Response(
                {"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# class CreatedepartmentView(SUAdmin_or_SuperuserMixin, APIView):
#     def get_department_name(self):
#         return f"department {Department.objects.filter(is_deleted = False).count() + 1}"

#     def post(self, request, *args, **kwargs):
#         members_static_ids = request.POST.getlist("member_ids")
#         if len(members_static_ids) == 0:
#             return Drf_Response(
#                 custom_response(message="No Members Selected"),
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         Item_id = request.POST["Item_id"]
#         department_leader_id = request.POST["department_leader"]
#         Item = Item.objects.filter(static_id=Item_id).first()

#         if not Item:
#             return Drf_Response(
#                 custom_response(message="No Such Item"),
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         if Item.available_space < len(members_static_ids):
#             return Drf_Response(
#                 custom_response(message="Too many members selected for the Item"),
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         try:
#             with transaction.atomic():
#                 department = department.objects.create(Item=Item, name=self.get_department_name())
#                 for static_id in members_static_ids:
#                     member = Member.objects.filter(static_id=static_id).first()
#                     if not member:
#                         raise ValueError("Invalid Member ID")
#                     if not department_leader_id:
#                         raise ValueError("No Leader Assigned")
#                     if static_id == department_leader_id:
#                         departmentMember.objects.create(
#                             member=member, department=department, is_leader=True
#                         )
#                     else:
#                         departmentMember.objects.create(member=member, department=department)
#                 return Drf_Response(
#                     custom_response(message="department Created Successfully", status=1),
#                     status=status.HTTP_200_OK,
#                 )
#         except ValueError as e:
#             message = str(e)
#             return Drf_Response(
#                 custom_response(message=message), status=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             message = str(e)
#             return Drf_Response(
#                 custom_response(message=message), status=status.HTTP_400_BAD_REQUEST
#             )


# add filtering to only pass members who aren't in a department / department_members havent been made


class ItemCreateView(SUAdmin_or_SuperuserMixin, CreateView):
    model = Item
    form_class = BaseForm
    template_name = "rec_create_Item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["Itemlist"] = ",".join(
            Item.objects.filter().values_list("name", flat=True)
        )
        return context

    def get_success_url(self) -> str:
        return reverse("create-Items")


class ItemAddListAPI(SUAdmin_or_SuperuserMixin, generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class ItemdepartmentMemberAPI(SUAdmin_or_SuperuserMixin, APIView):
    def post(self, request):
        item = get_object_or_404(Item, static_id=request.POST.get("item_id"))
        department_member = get_object_or_404(
            DepartmentMember, static_id=request.POST.get("member_id")
        )

        try:
            with transaction.atomic():
                rgp, created = ItemDepartmentMember.objects.get_or_create(
                    Item=item,
                    department_member=department_member
                )

                rgp.quantity += int(request.POST.get("quantity"))
                rgp.Item.total_issued += int(request.POST.get("quantity"))
                rgp.Item.total_stock -= int(request.POST.get("quantity"))
                rgp.Item.save()
                rgp.save()
                return Drf_Response({"message": "Issued successfully"})
                
        except Exception as e:
            return Drf_Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        members = request.POST.getlist("members[]")

        try:
            with transaction.atomic():
                ItemDepartmentMember.objects.filter(static_id__in=members).delete()

            return Drf_Response({"message": "Members deallocated successfully"})

        except Exception as e:
            return Drf_Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ItemdepartmentMemberReturnAPI(SUAdmin_or_SuperuserMixin, APIView):
    def post(self, request):
        itemlist = self.request.POST.getlist("itemlist")
        try:
            with transaction.atomic():
                for item in itemlist:
                    (rgp_static_id, quantity) = item.split(",")
                    rgp = get_object_or_404(ItemDepartmentMember, static_id=rgp_static_id)

                    if (rgp.quantity - int(quantity)) < 0:
                        raise ValueError("Return quantity is greater than issued quantity")
                    elif (rgp.quantity - int(quantity)) == 0:
                        rgp.Item.total_issued -= rgp.quantity
                        rgp.Item.total_stock += rgp.quantity
                        rgp.Item.save()
                        rgp.delete()
                    else:
                        rgp.Item.total_issued -= int(quantity)
                        rgp.Item.total_stock += int(quantity)
                        rgp.Item.save()
                        rgp.quantity -= int(quantity)
                        rgp.save()


            return Drf_Response({"message": "Returns done successfully"})

        except Exception as e:
            return Drf_Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartmentListAPI(SUAdmin_or_SuperuserMixin, generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DepartmentSerializer
    # queryset = department.objects.all()
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = DepartmentFilter

    def get_queryset(self):
        gp = DepartmentMember.objects.filter(
            Item_department_member=None, member__verified_by_controllz=True
        )
        queryset = Department.objects.all().filter(pk__in=gp.values_list("department", flat=True))
        return queryset


class departmentMemberListAPI(SUAdmin_or_SuperuserMixin, generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DepartmentMemberSerializer
    queryset = DepartmentMember.objects.filter()
    filter_backends = (dj_filters.DjangoFilterBackend,)


class ItemListView(
    SUAdmin_or_SuperuserMixin, SingleTableMixin, ExportMixin, FilterView
):
    model = Item
    table_class = ItemTable
    filterset_class = ItemFilter
    template_name = "Item_list_view.html"
    export_formats = ["csv"]
    exclude_columns = ("view",)
    export_name = "Items List"
    table_pagination = {"per_page": 8}

    def get_queryset(self):
        return super().get_queryset().order_by("name")
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["EditPage"] = False
        return context
    
class ItemEditView(ItemListView):
    table_class = ItemEditTable

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["EditPage"] = True
        return context
    
class EditItemsAPI(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                for item in request.POST.getlist("itemlist"):
                    (total_stock, static_id) = item.split(",")
                    item = Item.objects.get(static_id=static_id)
                    if not item:
                        raise ValueError("Invalid Item ID")
                    item.total_stock = int(total_stock)
                    item.save()
            return Drf_Response({"message": "Items updated successfully"})
        except Exception as e:
            return Drf_Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ItemDetailsView(SUAdmin_or_SuperuserMixin, SingleTableMixin, FilterView):
    model = Item
    table_class = ItemdepartmentMemberDetailsTable
    template_name = "Item_details.html"
    table_pagination = {"per_page": 10}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        item = Item.objects.filter(static_id=self.kwargs["static_id"]).first()
        context["Item_data"] = item
        return context

    def get_queryset(self):
        return (
            ItemDepartmentMember.objects.filter(
                is_deleted=False, Item__static_id=self.kwargs["static_id"]
            )
            .all()
            .order_by("department_member__member__profile__name")
        )


class ItemdepartmentMembersListView(
    SUAdmin_or_SuperuserMixin, SingleTableMixin, ExportMixin, FilterView
):
    model = ItemDepartmentMember
    table_class = AllocatedMembersTable
    template_name = "departmentmembers.html"
    # filterset_class = AllocatedMembersFilter
    export_formats = ["csv"]
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return super().get_queryset().order_by("department_member__member")


class departmentListView(SUAdmin_or_SuperuserMixin, SingleTableView):
    model = Department
    table_class = departmentListTable
    table_pagination = {"per_page": 10}
    template_name = "department-list.html"

    def get_queryset(self):
        return super().get_queryset().order_by("name")
    
class departmentDetailsView(SUAdmin_or_SuperuserMixin, SingleTableView):
    model = ItemDepartmentMember
    table_class = ItemdepartmentMemberDetailsTable
    table_pagination = {"per_page": 10}
    template_name = "department-details.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        department = Department.objects.filter(
            static_id=self.kwargs["static_id"], is_deleted=False
        ).first()
        context["department_data"] = department
        context["items_allocated"] = sum(ItemDepartmentMember.objects.filter(
            department_member__department = department
        ).values_list('quantity', flat=True))
        context["items"] = Item.objects.all()
        context["members"] = department.department_members.all().order_by("-is_leader")
        # context["department_leader"] = department.department_members.filter(is_leader=True).first()
        return context

    def get_queryset(self):
        return super().get_queryset().filter(department_member__department__static_id = self.kwargs["static_id"]).order_by("Item__name")
        # return (Item.objects.filter(Item_members__department_member__department__static_id = self.kwargs["static_id"]).distinct())

# class AllMembersView(
#     SUAdmin_or_SuperuserMixin, SingleTableMixin, ExportMixin, FilterView
# ):
#     model = departmentMember
#     table_class = AlldepartmentMembersTable
#     filterset_class = AlldepartmentMemberFilter
#     template_name = "rec_all_members.html"
#     export_formats = ["csv"]
#     table_pagination = {"per_page": 10}

#     def get_queryset(self):
#         return departmentMember.objects.filter(member__verified_by_controllz=True).order_by(
#             "member__profile__name"
#         )


# class departmentDetailsView(
#     SUAdmin_or_SuperuserMixin, SingleTableMixin, ExportMixin, FilterView
# ):
#     template_name = "rec_department_details.html"
#     model = departmentMember
#     table_class = departmentMembersTable
#     filterset_class = departmentDetailsFilter
#     export_formats = ["csv"]
#     table_pagination = {"per_page": 10}

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         department = department.objects.filter(
#             static_id=self.kwargs["static_id"], is_deleted=False
#         ).first()
#         context["department_data"] = department
#         context["department_leader"] = department.department_members.filter(is_leader=True).first()
#         return context

#     def get_queryset(self):
#         return (
#             departmentMember.objects.filter(
#                 member__verified_by_controllz=True,
#                 is_deleted=False,
#                 department__static_id=self.kwargs["static_id"],
#             )
#             .all()
#             .order_by("member__profile__name")
#         )

