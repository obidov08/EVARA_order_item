from django.shortcuts import render
from django.http import JsonResponse
from shop.models import Product



class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if not cart:
            cart = self.session['session_key']={}

        self.cart = cart

    def add(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            self.cart[product_id] += 1
        else:
            self.cart[product_id] = 1

        self.session.modified = True
    
    def get_quantity(self):
        return len(self.cart.keys())

    def get_product(self):
        product = []

        for pid in self.cart.keys():
            product.append(Product.objects.get(id=pid))
        
        return product

def add_to_cart(request, product_id):
    cart = Cart(request)

    if Product.objects.filter(id=product_id).exists():  
        cart.add(product_id)

    return JsonResponse({"message": "Savatga qo'shildi", "cart_count": cart.get_quantity()})


def get_cart_page(request):
    cart = Cart(request)

    products = cart.get_product()

    data = {
        "path": "Savatcha",
        "cart_count": cart.get_quantity(),
        "products": products
    }

    return render(request, "shop/cart.html", context=data) 