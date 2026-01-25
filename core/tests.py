from django.contrib.auth.models import User
from django.test import TestCase
from .models import Product, Category, Customer, Cart, CartItem
from .repositories import DjangoProductRepository, DjangoCartRepository
from .services import CartService
from .forms import AddressForm
from .facades import CustomerFacade
from unittest.mock import MagicMock, patch

#add fitness tests
#testy akceptacyjne
#---------------------------- Repository Tests ---------------------------

#Product tests
class ProductRepositoryTest(TestCase):
    def setUp(self):
        self.repo = DjangoProductRepository()
        self.category = Category.objects.create(title="Category", is_active=True)
        self.product = Product.objects.create(
            title="Initial Product",
            price=10,
            inventory=5,
            category=self.category
        )

    def test_save_product(self):
        new_product = Product(title="New", price=5, inventory=1, category=self.category)
        self.repo.save_product(new_product)
        self.assertTrue(Product.objects.filter(title="New").exists())

    def test_delete_product(self):
        self.repo.delete_product(self.product)
        self.assertEqual(Product.objects.count(), 0)

#Cart tests
class CartRepositoryTest(TestCase):
    def setUp(self):
        self.repo = DjangoCartRepository()
        self.category = Category.objects.create(title="Category", is_active=True)
        self.user = User.objects.create_user(username='test', password='<PASSWORD>', email='<EMAIL>', first_name='test',last_name='test')
        self.customer = Customer.objects.create(user=self.user, phone_number='+555555555')
        self.cart = Cart.objects.create(customer=self.customer)
        self.product = Product.objects.create(
            title="Initial Product",
            price=10,
            inventory=5,
            category=self.category
        )

    def test_add_to_cart(self):
        self.repo.add_item(self.user, self.product.id, 10)
        cart_item = CartItem.objects.get(cart=self.cart, product=self.product)
        self.assertEqual(cart_item.quantity, 10)

    def test_update_item_quantity(self):
        self.repo.add_item(self.user, self.product.id, 10)
        self.repo.update_item_qty(self.user, self.product, 5)
        cart_item = CartItem.objects.get(cart=self.cart, product=self.product)
        self.assertEqual(cart_item.quantity, 5)



#---------------------------- Services Tests ---------------------------
class CartServiceTest(TestCase):
    def setUp(self):
        self.repo = DjangoCartRepository()
        self.service = CartService(self.repo)
        self.user = User.objects.create_user(username='test', password='<PASSWORD>', email='<EMAIL>', first_name='test', last_name='test')
        self.customer = Customer.objects.create(user=self.user, phone_number='+555555555')
        self.cart = Cart.objects.create(customer=self.customer)
        self.category = Category.objects.create(title="Category", is_active=True)
        self.product = Product.objects.create(
            title="Initial Product",
            price=10,
            inventory=5,
            category=self.category
        )

    def test_add_to_cart(self):
        self.service.add_product(self.user, self.product.pk, 3)
        items = self.service.get_cart_items(self.user)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].quantity, 3)

    def test_update_item_quantity(self):
        self.service.add_product(self.user, self.product.pk, 1)
        self.service.update_quantity(self.user, self.product, 4)
        items = self.service.get_cart_items(self.user)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].quantity, 4)

    def test_remove_from_cart(self):
        self.service.add_product(self.user, self.product.pk, 1)
        self.service.remove_product(self.user, self.product.pk)
        items = self.service.get_cart_items(self.user)
        self.assertEqual(len(items), 0)

    def test_update_quantity_respects_inventory_limit(self):
        self.service.add_product(self.user, self.product.pk, 1)
        self.service.update_quantity(self.user, self.product, 10)
        items = self.service.get_cart_items(self.user)
        self.assertEqual(items[0].quantity, 5)

class CartServiceUnitTestMocks(TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = CartService(self.mock_repo)

    def test_update_quantity_caps_at_inventory(self):
        # Arrange
        user = MagicMock()
        product = MagicMock()
        product.inventory = 5 # Inventory is 5
        requested_qty = 10    # User wants 10

        self.service.update_quantity(user, product, requested_qty)
        self.mock_repo.update_item_qty.assert_called_once_with(user, product, 5)
#---------------------------- Facade Tests ---------------------------
class TestCustomerFacade(TestCase):

    def setUp(self):
        self.mock_cart_service = MagicMock()
        self.mock_order_service = MagicMock()
        self.mock_customer_service = MagicMock()
        self.mock_product_service = MagicMock()
        self.mock_address_service = MagicMock()
        self.mock_category_service = MagicMock()

        self.facade = CustomerFacade(
            cart_service=self.mock_cart_service,
            order_service=self.mock_order_service,
            customer_service=self.mock_customer_service,
            product_service=self.mock_product_service,
            address_service=self.mock_address_service,
            category_service=self.mock_category_service
        )

    @patch('django.db.transaction.atomic')
    def test_add_product_calls_service_correctly(self, mock_atomic):
        user = MagicMock(id=1)
        product_id = 101
        quantity = 2

        self.facade.add_product(user, product_id, quantity)
        mock_atomic.assert_called_once()
        self.mock_cart_service.add_product.assert_called_once_with(user, product_id, quantity)
#---------------------------- Forms Tests ---------------------------
class AddressFormTest(TestCase):
    def test_address_form_valid_data(self):
        form_data = {
            'street_address': 'ul. Wiejska 1',
            'city': 'Warszawa',
            'zip_code': '00-000'
        }
        form = AddressForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_address_form_invalid_data(self):
        form_data = {
            'street_address': 'ul. Wiejska 1',
            'city': 'Warszawa',
            'zip_code': '00001'
        }
        form = AddressForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_address_form_missing_data(self):
        form_data = {
            'street_address': 'ul. Wiejska 1',
            'city': '',
            'zip_code': '00-001'
        }
        form = AddressForm(data=form_data)
        self.assertFalse(form.is_valid())