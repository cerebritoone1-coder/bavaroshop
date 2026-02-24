from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.conf.urls.static import static


# 🔥 RESET ADMIN TEMPORAL
def reset_admin(request):
    if request.GET.get("key") != "2026":
        return HttpResponse("Forbidden", status=403)

    User = get_user_model()

    user, created = User.objects.get_or_create(
        username="admin",
        defaults={"email": "cerebritoone1@gmail.com"}
    )

    user.set_password("marino19870603")
    user.is_staff = True
    user.is_superuser = True
    user.save()

    return HttpResponse("ADMIN RESETEADO OK")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.store.urls')),

    # 🔥 RUTA SECRETA
    path('reset-admin-2026/', reset_admin),
]

# 👇 MEDIA SOLO EN DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)