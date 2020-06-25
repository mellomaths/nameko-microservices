class Helper:

    @staticmethod
    def calculate_new_cart_total_price(cart, new_product):
        new_product_price = new_product['price'] * new_product['amount']
        total_price = cart['total_price'] + new_product_price
        return total_price
