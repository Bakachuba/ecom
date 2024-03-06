from django.http import request, JsonResponse
from django.shortcuts import render, get_object_or_404

from cart.cart import Cart
from store.models import Product


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    return render(request, 'cart/cart_summary.html', {'cart_products': cart_products, 'quantities': quantities})


def cart_add(request):
    # Get the cart
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get Stuff
        product_id = int(request.POST.get('product_id'))
        product_qrt = int(request.POST.get('product_qty'))

        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save to session
        cart.add(product=product, quantity=product_qrt)

        # Get cart quantity
        cart_quantity = cart.__len__()

        # Return response
        # response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'qty': cart_quantity})

        return response


def cart_delete(request):
    pass


def cart_update(request):
    pass
