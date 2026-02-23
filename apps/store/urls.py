from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView, RegisterView

urlpatterns = [

    # ==========================
    # HOME Y TIENDA
    # ==========================
    path('', views.home, name='home'),
    path('tienda/', views.tienda, name='tienda'),
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),

    # ==========================
    # AUTENTICACIÓN
    # ==========================
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', views.custom_logout, name='logout'),

    # ==========================
    # PERFIL
    # ==========================
   
   
 

    # ==========================
    # NOTIFICACIONES
    # ==========================
 
 

    # ==========================
    # RECUPERAR CONTRASEÑA
    # ==========================
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

    # ==========================
    # CHECKOUT
    # ==========================
    path('checkout-direccion/', views.checkout_direccion, name='checkout_direccion'),
    path('datos-transferencia/', views.datos_transferencia, name='datos_transferencia'),
    path('pedido-confirmado/', views.pedido_confirmado, name='pedido_confirmado'),

    # ==========================
    # PEDIDOS
    # ==========================
    path('eliminar-pedido/<int:pedido_id>/', views.eliminar_pedido, name='eliminar_pedido'),
]