from typing import Any

from django.db.models.sql.datastructures import Empty

from .interfaces import ICartRepository, IProductRepository, ICartService, \
    IProductService, ICategoryService, ICategoryRepository, IAddressService, IAddressRepository, IOrderService, \
    IOrderRepository, ICustomerService, ICustomerRepository


class ProductService(IProductService):
    def __init__(self, repo: IProductRepository):
        self.repo = repo

    def get_products_for_display(self):
        return self.repo.get_all()

    def get_product(self, product_id):
        if product_id is None: return None
        return self.repo.get_product(product_id)

    def get_product_inventory(self, product_id) -> int:
        if product_id is None: return 0
        product = self.repo.get_product(product_id)
        return getattr(product, 'inventory', 0)

    def save_product(self, product):
        self.repo.save_product(product)

    def delete_product(self, product, is_linked):
        if is_linked:
            product.is_active = False
            self.repo.save_product(product)
        else:
            self.repo.delete_product(product)

    def update_product_inventory(self, product, quantity):
        product.inventory = product.inventory - quantity
        self.repo.save_product(product)

    def is_category_linked_to_active_product(self, category):
        return self.repo.category_has_active_products(category)

    def is_category_linked_to_any_product(self, category):
        return self.repo.category_has_products(category)

class OrderService(IOrderService):
    def __init__(self, repo: IOrderRepository):
        self.repo = repo

    def is_address_linked_to_order(self, address):
        return self.repo.address_has_orders(address)

    def is_product_linked_to_order(self, product):
        return self.repo.product_has_orders(product)

    def get_user_orders(self, user):
        orders =  self.repo.get_user_orders(user)

        formatted_data = []

        for order in orders:
            order_items = self.repo.get_order_items(order)

            entry = {
                "order_details": order,
                "items": order_items
            }

            formatted_data.append(entry)

        return formatted_data

    def get_all(self):
        return self.repo.get_all()

    def send_order(self, pk):
        order = self.repo.get_order(pk)
        order.order_status = 'S'
        self.repo.save_order(order)

    def complete_order(self, pk):
        order = self.repo.get_order(pk)
        order.order_status = 'C'
        self.repo.save_order(order)

    def create_order(self, customer, address_id):
        return self.repo.create_order(customer, address_id)

    def add_to_order(self, order, item):
        self.repo.add_item(order, item)





class CustomerService(ICustomerService):
    def __init__(self, repo: ICustomerRepository):
        self.repo = repo

    def get_customer(self, user):
        return self.repo.get_customer(user)

class AddressService(IAddressService):
    def __init__(self, repo: IAddressRepository):
        self.repo = repo

    def get_user_addresses(self, user):
        return self.repo.get_user_addresses(user)

    def get_address(self, address_id):
        return self.repo.get_address(address_id)

    def save_address(self, address):
        self.repo.save_address(address)

    def delete_address(self, address, is_linked):
        if is_linked:
            address.is_active = False
            self.repo.save_address(address)
        else:
            self.repo.delete_address(address)


class CartService(ICartService):
    def __init__(self, repo: ICartRepository):
        self.repo = repo

    def is_cart_empty(self, user):
        return self.repo.get_cart_items(user).count() == 0

    def get_cart_details(self, user):
        items = self.repo.get_cart_items(user)
        total_val = sum(item.quantity * item.product.price for item in items)
        count = sum(item.quantity for item in items)
        return {
            'items': items,
            'total_value': total_val,
            'count': count
        }

    def add_product(self, user, product_id, quantity):
        self.repo.add_item(user, product_id, quantity)

    def update_quantity(self, user, product, quantity):
        inventory = getattr(product, 'inventory', 0)

        final_qty = min(quantity, inventory)
        self.repo.update_item_qty(user, product, final_qty)

    def remove_product(self, user, product_id):
        self.repo.remove_item(user, product_id)

    def remove_product_from_all_carts(self, product):
        self.repo.remove_product_from_all_carts(product)

    def get_cart_items(self, user):
        return self.repo.get_cart_items(user)


class CategoryService(ICategoryService):
    def __init__(self, repo: ICategoryRepository):
        self.repo = repo

    def get_categories(self):
        return self.repo.get_all()

    def get_category(self, category_id):
        if category_id is None: return None
        return self.repo.get_category(category_id)

    def save_category(self, category):
        self.repo.save_category(category)

    def delete_category(self, category, is_active_linked, is_linked):
        if is_active_linked:
            raise ValueError("Cannot delete category: It contains active products. Please deactivate products first.")
        elif is_linked:
            category.is_active = False
            self.repo.save_category(category)
        else:
            self.repo.delete_category(category)