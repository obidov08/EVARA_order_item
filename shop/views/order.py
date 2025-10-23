from django.shortcuts import redirect, render
from django.views.generic import View
from shop.models import OrderItem, Order
from shop.views import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from asgiref.sync import async_to_sync
from shop.telegram import send_message


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
        
        order_text = self.get_order_text(items, user, address, additional, order)
        async_to_sync(send_message)(order_text)    

        return redirect("dashboard")
    

    def get_order_text(self, items, user, address, additional, order):
        order_text = f"<b>📦 Yangi buyurtma!</b>\n\n"
        order_text += f"<b>👤 Foydalanuvchi:</b> {user.username}\n"
        order_text += f"<b>📧 Email:</b> {user.email if user.email else 'Mavjud emas'}\n"
        order_text += f"<b>🏠 Manzil:</b> {address}\n"
        order_text += f"<b>📦 Qo'shimcha ma'lumot:</b> {additional}\n"
        order_text += f"<b>⏰ Sana:</b> {order.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        order_text += f"<b>✅ Holat:</b> {order.get_status_display()}\n"
        order_text += f"<b>🛒 Buyurtma tarkibi:</b>\n\n"

        total_sum = 0
        for item in items:
            p = item.product
            line = f" - {p.name} | Soni: {item.quantity} | Narx: {item.total_price} so'm\n"
            order_text += line
            total_sum += item.total_price

        order_text += f"\n<b>💰 Umumiy summa:</b> ${total_sum}"
