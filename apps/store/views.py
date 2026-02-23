from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy
from decimal import Decimal

from .models import Product, Order, OrderItem


# ==========================
# HOME (PÚBLICA)
# ==========================
def home(request):
    return render(request, 'store/home.html')


# ==========================
# TIENDA (PÚBLICA)
# ==========================
def tienda(request):
    query = request.GET.get('q')
    productos = Product.objects.filter(is_active=True)

    if query:
        productos = productos.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'store/tienda.html', {
        'productos': productos,
    })


# ==========================
# DETALLE PRODUCTO (PÚBLICO)
# ==========================
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    sizes = product.sizes.all()
    images = product.images.all()

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


# ==========================
# AGREGAR AL CARRITO
# ==========================
def agregar_al_carrito(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size_selected = request.POST.get('size')

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
def ver_carrito(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())

    return render(request, 'store/carrito.html', {
        'cart': cart,
        'total': total
    })


# ==========================
# ELIMINAR PRODUCTO DEL CARRITO
# ==========================
def eliminar_carrito(request, key):
    cart = request.session.get('cart', {})

    if key in cart:
        if cart[key]['quantity'] > 1:
            cart[key]['quantity'] -= 1
        else:
            del cart[key]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('ver_carrito')


# ==========================
# CHECKOUT (SIN LOGIN)
# ==========================
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

        # CREAR ORDEN SIN USUARIO
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            phone=phone,
            total_amount=total,
            payment_method=payment_method,
            status=status
        )

        for key, item in cart.items():
            product_id = key.split("-")[0]
            product = Product.objects.get(id=product_id)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=product.price
            )

        del request.session['cart']
        request.session.modified = True

        if payment_method == "transfer":
            return redirect('datos_transferencia')
        else:
            return redirect('pedido_confirmado')

    return render(request, "store/checkout_direccion.html", {
        "total": total
    })


# ==========================
# DATOS TRANSFERENCIA
# ==========================
def datos_transferencia(request):
    return render(request, "store/datos_transferencia.html")


# ==========================
# PEDIDO CONFIRMADO
# ==========================
def pedido_confirmado(request):
    return render(request, "store/pedido_confirmado.html")