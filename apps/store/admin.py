from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    Product,
    ProductSize,
    Profile,
    Order,
    OrderItem,
    ProductImage
)


# ==========================
# PRODUCT SIZE INLINE
# ==========================
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1


# ==========================
# PRODUCT IMAGE INLINE (GALERÍA)
# ==========================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# ==========================
# ORDER ITEM INLINE (PRODUCTOS DENTRO DEL PEDIDO)
# ==========================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False


# ==========================
# PRODUCT ADMIN
# ==========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active', 'created')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

    # 👇 AQUÍ YA NO DA ERROR
    inlines = [ProductSizeInline, ProductImageInline]


# ==========================
# CATEGORY ADMIN
# ==========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


# ==========================
# PROFILE ADMIN
# ==========================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'notifications', 'two_factor_enabled')
    search_fields = ('user__email',)


# ==========================
# ORDER ADMIN
# ==========================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'first_name',
        'last_name',
        'city',
        'phone',
        'payment_method',
        'colored_status',
        'total_amount',
        'created_at',
        'short_address',
    )

    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('first_name', 'last_name', 'city', 'phone')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]
    actions = ['eliminar_pedidos_seleccionados']

    fieldsets = (
        ("🧾 Información del Pedido", {
            'fields': (
                'created_at',
                'status',
                'payment_method',
                'total_amount',
            )
        }),
        ("👤 Información Completa del Cliente", {
            'fields': (
                'user',
                'first_name',
                'last_name',
                'phone',
                'address',
                'city',
            )
        }),
    )

    # ========= Dirección corta =========
    def short_address(self, obj):
        if not obj.address:
            return "-"
        return obj.address if len(obj.address) <= 40 else obj.address[:40] + "..."

    short_address.short_description = "Dirección"

    # ========= Estado con color =========
    def colored_status(self, obj):
        colors = {
            'pending': 'orange',
            'pending_payment': 'red',
            'paid': 'green',
            'delivered': 'blue',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color:{}; font-weight:600;">{}</span>',
            color,
            obj.status
        )

    colored_status.short_description = "Estado"

    # ========= Acción eliminar =========
    def eliminar_pedidos_seleccionados(self, request, queryset):
        queryset.delete()

    eliminar_pedidos_seleccionados.short_description = "🗑 Eliminar pedidos seleccionados"

    # ========= No permitir crear pedidos manualmente =========
    def has_add_permission(self, request):
        return False
