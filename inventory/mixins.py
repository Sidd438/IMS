from django.shortcuts import redirect

from .models import SUUser


class SUAdmin_or_SuperuserMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            elif SUUser.objects.filter(auth_user=self.request.user).exists():
                return super().dispatch(request, *args, **kwargs)
        return redirect("rec-login-page")
