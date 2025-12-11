from .interfaces import ICartService, IOrderService, ICustomerService, IProductService, IAddressService, \
    ICategoryService, ICustomerFacade, IEmployeeFacade


class CustomerFacade(ICustomerFacade):
    def __init__(self,
                 cart_service: ICartService,
                 order_service: IOrderService,
                 customer_service: ICustomerService,
                 product_service: IProductService,
                 address_service: IAddressService,
                 category_service: ICategoryService):
        self.cart_service = cart_service
        self.order_service = order_service
        self.customer_service = customer_service
        self.product_service = product_service
        self.address_service = address_service
        self.category_service = category_service

    # =====================PRODUCTS=====================

    def get_products_for_display(self):
        return self.product_service.get_products_for_display()

    # =====================ORDERS=====================
    def get_user_orders(self, user):
        return self.order_service.get_user_orders(user)

    def checkout(self, user, address):
        customer = self.customer_service.get_customer(user)
        order = self.order_service.create_order(customer, address)

        cart_items = self.cart_service.get_cart_items(user)
        for item in cart_items:
            self.order_service.add_to_order(order, item)
            self.cart_service.remove_product(user, item.product.id)
            product = self.product_service.get_product(item.product.id)
            self.product_service.update_product_inventory(product, item.quantity)


    # =====================CUSTOMER=====================

    def get_customer(self, user):
        return self.customer_service.get_customer(user)

    # =====================ADDRESS=====================

    def get_customer_address(self, user):
        return self.address_service.get_user_addresses(user)

    def get_address(self, address_id):
        return self.address_service.get_address(address_id)

    def save_address(self, user, address):
        address.customer = self.customer_service.get_customer(user)
        self.address_service.save_address(address)

    def delete_address(self, address):
        is_linked = self.order_service.is_address_linked_to_order(address)
        self.address_service.delete_address(address, is_linked)

    # =====================CART=====================
    def get_cart_details(self, user):
        return self.cart_service.get_cart_details(user)

    def add_product(self, user, product_id, quantity):
        self.cart_service.add_product(user, product_id, quantity)

    def update_quantity(self, user, product_id, quantity):
        product = self.product_service.get_product(product_id)
        self.cart_service.update_quantity(user, product, quantity)

    def remove_product(self, user, product_id):
        self.cart_service.remove_product(user, product_id)

class EmployeeFacade(IEmployeeFacade):
    def __init__(self,
                 cart_service: ICartService,
                 order_service: IOrderService,
                 customer_service: ICustomerService,
                 product_service: IProductService,
                 address_service: IAddressService,
                 category_service: ICategoryService):
        self.cart_service = cart_service
        self.order_service = order_service
        self.customer_service = customer_service
        self.product_service = product_service
        self.address_service = address_service
        self.category_service = category_service

    # =====================PRODUCTS=====================
    def get_all_products(self):
        return self.product_service.get_products_for_display()

    def get_product(self, product_id):
        return self.product_service.get_product(product_id)

    def save_product(self, product_id):
         self.product_service.save_product(product_id)

    def delete_product(self, product_id):
         product = self.product_service.get_product(product_id)
         is_linked = self.order_service.is_product_linked_to_order(product)
         self.cart_service.remove_product_from_all_carts(product)
         self.product_service.delete_product(product, is_linked)

    # =====================ORDERS=====================

    def get_all_orders(self):
        return self.order_service.get_all()

    def send_order(self, order_id):
        self.order_service.send_order(order_id)

    def complete_order(self, order_id):
        self.order_service.complete_order(order_id)

    # =====================CATEGORY=====================

    def get_categories(self):
        return self.category_service.get_categories()

    def get_category(self, category_id):
        return self.category_service.get_category(category_id)

    def save_category(self, category):
        self.category_service.save_category(category)

    def delete_category(self, category_id):
        category = self.category_service.get_category(category_id)
        is_active_linked = self.product_service.is_category_linked_to_active_product(category)
        is_linked = self.product_service.is_category_linked_to_any_product(category)
        self.category_service.delete_category(category, is_active_linked, is_linked)



