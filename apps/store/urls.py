from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView, RegisterView

urlpatterns = [

    # ==========================
    # HOME Y TIENDA
    # ==========================
    path('', views.home, name='home'),
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),

    path('tienda/', views.tienda, name='tienda'),

    # ==========================
    # AUTENTICACIÓN
    # ==========================
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # ==========================
    # PERFIL
    # ==========================
    path('mi-perfil/', views.mi_perfil, name='mi_perfil'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('direcciones/', views.direcciones, name='direcciones'),

    # ==========================
    # NOTIFICACIONES
    # ==========================
    path('notificaciones/', views.notificaciones_web, name='notificaciones_web'),
    path('notificacion/<int:id>/', views.marcar_notificacion, name='marcar_notificacion'),

    path(
    'notificacion/eliminar/<int:id>/',
    views.eliminar_notificacion,
    name='eliminar_notificacion'
),


    # ==========================
    # CAMBIAR CONTRASEÑA (PROPIO)
    # ==========================
    path(
        'cambiar-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='store/cambiar_password.html',
            success_url='/cambiar-password/exito/'
        ),
        name='password_change'
    ),

    path(
        'cambiar-password/exito/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='store/cambiar_password_exito.html'
        ),
        name='password_change_done'
    ),

    # ==========================
# RECUPERAR CONTRASEÑA
# ==========================

path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='store/password_reset.html',
        email_template_name='store/password_reset_email.html',
        success_url='/password-reset/done/'
    ),
    name='password_reset'
),

path(
    'password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='store/password_reset_done.html'
    ),
    name='password_reset_done'
),

path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='store/password_reset_confirm.html',
        success_url='/reset/done/'
    ),
    name='password_reset_confirm'
),

path(
    'reset/done/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='store/password_reset_complete.html'
    ),
    name='password_reset_complete'
),

# ==========================
# CARRITO
# ==========================
path('carrito/', views.ver_carrito, name='ver_carrito'),
path('agregar-al-carrito/<int:product_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
path('eliminar/<str:key>/', views.eliminar_carrito, name='eliminar_carrito'),

path("checkout-direccion/", views.checkout_direccion, name="checkout_direccion"),

path("datos-transferencia/", views.datos_transferencia, name="datos_transferencia"),
path("pedido-confirmado/", views.pedido_confirmado, name="pedido_confirmado"),

path('eliminar-pedido/<int:pedido_id>/', views.eliminar_pedido, name='eliminar_pedido'),

]
