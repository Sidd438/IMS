from django.contrib.auth import views as auth_views
from django.urls import path


from .views import *

urlpatterns = [
    path("login/", SUUserLoginView, name="rec-login-page"),
    path("logout/", auth_views.LogoutView.as_view(), name="rec-logout"),
    path("create-departments/", AllocateItemTemplate.as_view(), name="allocate-Items"),
    # path("create-departments-post/", CreatedepartmentView.as_view(), name="create-departments-post"),
    # path("all-members-rec/", AllMembersView.as_view(), name="all-members-rec"),
    # path(
    #     "create-departments-fetch/",
    #     ApprovedMembersListView.as_view(),
    #     name="create-departments-fetch",
    # ),
    ##############################################################################
    path("create-Item/", ItemCreateView.as_view(), name="create-Item"),
    path(
        "Item-department-members/",
        ItemdepartmentMemberAPI.as_view(),
        name="rec-Item-department-member-api",
    ),
    path(
        "Item-department-members/return",
        ItemdepartmentMemberReturnAPI.as_view(),
        name="rec-Item-department-member-return",
    ),
    path("Items/", ItemAddListAPI.as_view(), name="Items"),
    path("ItemAvailability/", ItemAvailabilityAPI.as_view(), name="Item-Availability"),
    # path("departments/", departmentListAPI.as_view(), name="rec-departments"),
    path("departments/members/", departmentMemberListAPI.as_view(), name="departments-members"),
    # path("colleges/", CollegeListAPI.as_view(), name="rec-colleges"),
    # path(
    #     "create-Items-fetch",
    #     AppliedMembersSelectView.as_view(),
    #     name="create-Items-fetch",
    # ),
    # path("get-Item-data/", GetItemDataAPIView.as_view(), name="get-Item-data"),
    # path("get-item-detail/", GetItemDetailAPIView.as_view(), name="get-item-detail"),
    # path("get-Item-detail/", GetItemDetailAPIView.as_view(), name="get-Item-detail"),
    path("Item-list/", ItemListView.as_view(), name="Item-list"),
    path(
        "Item-details/<str:static_id>", ItemDetailsView.as_view(), name="Item-details"
    ),
    path(
        "allocated-members/",
        ItemdepartmentMembersListView.as_view(),
        name="allocated-members",
    ),
    path("department-list/", departmentListView.as_view(), name="department-list"),
    path("department-details/<str:static_id>/", departmentDetailsView.as_view(), name="department-details"),
    # path(
    #     "department-details/<str:static_id>",
    #     departmentDetailsView.as_view(),
    #     name="department-details",
    # ),
    # path("issue-item/", IssueItemAPIView.as_view(), name="issue-item"),
    # path("return-item/", ReturnItemAPIView.as_view(), name="return-item"),
    # path("inventory/", Inventory.as_view(), name="inventory"),
    # path("create-inventory/", CreateInventory.as_view(), name="create-inventory"),
    # path("", SUDashboardView.as_view(), name="SU-dashboard"),
]
