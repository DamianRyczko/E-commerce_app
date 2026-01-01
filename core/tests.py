from django.contrib.auth.models import User
from django.test import TestCase
from .models import Product, Category, Customer, Cart
from .repositories import DjangoProductRepository, DjangoCartRepository
from .services import CartService
from .forms import AddressForm

#---------------------------- Repository Tests ---------------------------
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

#---------------------------- Forms Tests ---------------------------
class AddressFormTest(TestCase):
    def test_address_form_valid_data(self):
        form_data = {
            'street_address': 'ul. Wiejska 1',
            'city': 'Warszawa',
            'zip_code': '00-001'
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