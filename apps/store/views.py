from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout

from .forms import CustomUserCreationForm
from .models import Notification
from django.shortcuts import get_object_or_404
from .models import Product
from django.db.models import Q



from decimal import Decimal
from .models import Order
from .models import Order, OrderItem, Product







# ==========================
# HOME (PÚBLICA)
# ==========================
def home(request):
    return render(request, 'store/home.html')


def tienda(request):
    query = request.GET.get('q')
    productos = Product.objects.filter(is_active=True)

    if query:
        productos = productos.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
    else:
        unread_count = 0

    return render(request, 'store/tienda.html', {
        'productos': productos,
        'unread_count': unread_count
    })





# ==========================
# LOGIN PERSONALIZADO
# ==========================
class CustomLoginView(LoginView):
    template_name = 'store/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = False


    def get_success_url(self):
        return reverse_lazy('tienda')


# ==========================
# LOGOUT PERSONALIZADO
# ==========================
def custom_logout(request):
    logout(request)
    return redirect('home')


# ==========================
# REGISTRO
# ==========================
class RegisterView(CreateView):
    template_name = 'store/register.html'
    form_class = CustomUserCreationForm


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('tienda')
   
@login_required
def mis_pedidos(request):
    pedidos = request.user.orders.all().order_by('-created_at')

    return render(request, 'store/mis_pedidos.html', {
        'pedidos': pedidos
    })




# ==========================
# MIS PEDIDOS
# ==========================
@login_required
def mis_pedidos(request):
    pedidos = request.user.orders.all().order_by('-created_at')
    return render(request, 'store/mis_pedidos.html', {
        'pedidos': pedidos
    })




# ==========================
# DIRECCIONES
# ==========================
@login_required
def direcciones(request):
    unread_count = request.user.notifications.filter(is_read=False).count()
    return render(request, 'store/direcciones.html', {
        'unread_count': unread_count
    })


# ==========================
# NOTIFICACIONES WEB
# ==========================
@login_required
def notificaciones_web(request):
    notifications = request.user.notifications.all()
    return render(request, 'store/notificaciones_web.html', {
        'notifications': notifications
    })


@login_required
def marcar_notificacion(request, id):
    notification = Notification.objects.get(id=id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notificaciones_web')

from django.contrib.auth import login
from .models import Notification


# ==========================
# LOGIN PERSONALIZADO
# ==========================
class CustomLoginView(LoginView):
    template_name = 'store/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = False

    def form_valid(self, form):
        response = super().form_valid(form)

        # Crear notificación de bienvenida
        Notification.objects.create(
            user=self.request.user,
            message="Bienvenido nuevamente a MixShop 🎉"
        )

        return response

    def get_success_url(self):
        return reverse_lazy('tienda')

    
    # ==========================
# ELIMINAR NOTIFICACIÓN
# ==========================
@login_required
def eliminar_notificacion(request, id):
    notification = Notification.objects.get(id=id, user=request.user)
    notification.delete()
    return redirect('notificaciones_web')

# ==========================
# CARRITO
# ==========================
@login_required
def agregar_al_carrito(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    size_selected = request.POST.get('size')

    # 🔒 Si el producto tiene tallas y no se eligió ninguna → NO permitir
    if product.sizes.exists() and not size_selected:
        return redirect('product_detail', slug=product.slug)

    cart = request.session.get('cart', {})

    key = f"{product_id}-{size_selected}" if size_selected else str(product_id)

    if key in cart:
        cart[key]['quantity'] += 1
    else:
        cart[key] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'size': size_selected if size_selected else '',
            'image': product.image.url if product.image else ''
        }

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('ver_carrito')


# ==========================
# VER CARRITO
# ==========================
@login_required
def ver_carrito(request):
    cart = request.session.get('cart', {})
    total = 0

    for key, item in cart.items():
        total += float(item['price']) * item['quantity']

    return render(request, 'store/carrito.html', {
        'cart': cart,
        'total': total
    })


# ==========================
# ELIMINAR PRODUCTO DEL CARRITO
# ==========================
@login_required
def eliminar_carrito(request, key):
    cart = request.session.get('cart', {})

    if key in cart:
        if cart[key]['quantity'] > 1:
            # Solo restar 1
            cart[key]['quantity'] -= 1
        else:
            # Si es 1, eliminar completamente
            del cart[key]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('ver_carrito')


@login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    sizes = product.sizes.all()

    # 🔥 Imágenes adicionales
    images = product.images.all()

    # 🔥 Productos similares (misma categoría)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    return render(request, 'store/product_detail.html', {
        'product': product,
        'sizes': sizes,
        'images': images,
        'related_products': related_products
    })


@login_required
def checkout_direccion(request):

    cart = request.session.get('cart', {})
    if not cart:
        return redirect('ver_carrito')

    total = sum(float(item['price']) * item['quantity'] for item in cart.values())

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        phone = request.POST.get("phone")
        payment_method = request.POST.get("payment_method")

        if payment_method == "transfer":
            status = "pending_payment"
        else:
            status = "pending"

        # 🔥 CREAR ORDEN
        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            phone=phone,
            total_amount=total,
            payment_method=payment_method,
            status=status
        )

        # 🔥 GUARDAR PRODUCTOS EN OrderItem
        for key, item in cart.items():

            product_id = key.split("-")[0]
            product = Product.objects.get(id=product_id)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=product.price
            )

        # 🔥 VACIAR CARRITO
        del request.session['cart']
        request.session.modified = True

        # 🔥 REDIRECCIÓN
        if payment_method == "transfer":
            return redirect('datos_transferencia')
        else:
            return redirect('pedido_confirmado')

    return render(request, "store/checkout_direccion.html", {
        "total": total
    })

def mi_perfil(request):
    pedidos = request.user.orders.all().order_by('-created_at')
    return render(request, 'store/mi_perfil.html', {
        'pedidos': pedidos
    })

@login_required
def datos_transferencia(request):
    return render(request, "store/datos_transferencia.html")



def pedido_confirmado(request):
    return render(request, "store/pedido_confirmado.html")

@login_required
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Order, id=pedido_id, user=request.user)
    pedido.delete()
    return redirect('mis_pedidos')