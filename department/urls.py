from django.contrib.auth import views as auth_views
from django.urls import path


from .views import *

urlpatterns = [
    path("login/", DepartmentUserLoginView, name="dep-login-page"),
    path("", DepartmentDashboardView.as_view(), name="dep-dashboard")
]
