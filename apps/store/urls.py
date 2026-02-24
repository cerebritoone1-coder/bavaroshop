from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import get_user_model


# 🔥 RESET ADMIN DEFINITIVO
def reset_admin(request):
    if request.GET.get("key") != "2026":
        return HttpResponse("Forbidden", status=403)

    User = get_user_model()

    user, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "cerebritoone1@gmail.com"
        }
    )

    user.set_password("marino19870603")
    user.is_staff = True
    user.is_superuser = True
    user.save()

    return HttpResponse("ADMIN RESETEADO OK")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.store.urls')),

    # 🔥 ESTA RUTA VA AQUÍ
    path('reset-admin-2026/', reset_admin),
]