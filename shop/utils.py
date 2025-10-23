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

    def remove(self, product_id):
        if str(product_id) in self.cart.keys():
            del self.cart[str(product_id)] 
            self.session.modified = True
            return True
        return False

    def get_quantity(self):
        return len(self.cart.keys())

    def get_product(self):
        products = []

        for pid, quantity in self.cart.items():
            pd = Product.objects.get(id=pid)

            if pd.discount>0 and pd.discount_price is not None:
                total = pd.discount_price*quantity
            else:
                total = pd.price*quantity

            total_with_discount = total

            product = {
                "quantity": quantity,
                "data": Product.objects.get(id=pid),
                "total": total,
            }
            products.append(product)

        total_price = 0
        for product in products:
            total_price+=product['data'].price*product['quantity']

        data = {
            "product": products,
            "total_price": total_price,
            "total_with_discount": total_with_discount,
            "profit": total_price-total_with_discount
        }
        
        return data
    
    def clear(self):
        self.cart.clear()
        self.session.modified = True
   