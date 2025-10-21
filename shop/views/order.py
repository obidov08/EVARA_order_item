from django.shortcuts import redirect, render
from django.views.generic import View
from shop.models import OrderItem, Order
from shop.views import Cart
from django.contrib.auth.mixins import LoginRequiredMixin


class GetCheckoutPage(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        prodocts = cart.get_product()
        data = {
            "path": "Checkout",
            "cart_count": cart.get_quantity(),
            "products": prodocts
        }
        return render(request, "shop/checkout.html", context=data)
    
    def post(self, request):
        user = request.user
        cart = Cart(request)
        products = cart.get_product()
        address = request.POST.get('address', "Mavjud emas")
        additional = request.POST.get('additional', "Mavjud emas")
        print(request.POST)

        items=[]

        for product in products['products']:
            item, created = OrderItem.objects.get_or_create(
                product=product['data'],
                quantity=product['quantity'],
                total_price=product['total']
            )
            items.append(item)

        order = Order(user=user, address=address, additional_info=additional)
        order.save()
        order = items.add(*items)
        cart.clear()
        

        return redirect("dashboard")
