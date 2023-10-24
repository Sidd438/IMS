from django.shortcuts import redirect

from .models import DepartmentUser

class DepAdmin_or_SuperuserMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return redirect("department-details")
            elif DepartmentUser.objects.filter(auth_user=self.request.user).exists():
                return super().dispatch(request, *args, **kwargs)
        return redirect("dep-login-page")
