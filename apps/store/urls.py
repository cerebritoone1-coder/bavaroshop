from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # HOME Y TIENDA
    # ==========================
    path('', views.home, name='home'),
    path('tienda/', views.tienda, name='tienda'),
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),

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

]